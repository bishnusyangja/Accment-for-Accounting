from django.db import models

from users.models import Company, User
from ledger.models import Account, JournalEntry, set_transactions
from inventory.models import InventoryAccount, InventoryLedger
from lib import get_next_voucher_no, zero_for_none
from django.contrib.contenttypes.models import ContentType
import watson


class DayJournal(models.Model):
    voucher_no = models.IntegerField()
    date = models.DateField()
    company = models.ForeignKey(Company)
    cash_deposit = models.FloatField()
    cash_withdrawal = models.FloatField()
    cheque_deposit = models.FloatField()
    cash_actual = models.FloatField()
    lotto_sales_dispenser_amount = models.FloatField(default=0)
    # scratch_off_sales_dispenser_amount = models.FloatField(default=0)
    lotto_sales_register_amount = models.FloatField(default=0)
    scratch_off_sales_register_amount = models.FloatField(default=0)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')
    register_sales_amount = models.FloatField(default=0)
    register_sales_tax = models.FloatField(default=0)
    scratch_off_sales_manual = models.FloatField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(DayJournal, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(DayJournal, self.company)

    def get_total_deposits(self):
        total = 0.0
        for item in self.deposits.all():
            if str(item.deposit_from.category.name) == 'Cash Account':
                total += item.amount
        return total

    def get_total_cash_sales(self):
        total = 0.0
        for item in self.cash_sales.all():
            total += item.amount
        return total

    def get_total_summary_transfer(self):
        total = 0.0
        for item in self.summary_transfer.all():
            total += item.cash
        return total

    def get_total_card_sales(self):
        total = 0.0
        for item in self.card_sales.all():
            total += item.amount
        return total

    def get_total_cash_equivalent_sales(self):
        total = 0.0
        for item in self.cash_equivalent_sales.all():
            total += item.amount
        return total

    def get_total_vendor_payouts(self):
        total = 0.0
        for item in self.vendor_payout.all():
            if str(item.paid.category.name) == 'Cash Account':
                total += item.amount
        return total

    def get_total_other_payouts(self):
        total = 0.0
        for item in self.other_payout.all():
            if str(item.paid.category.name) == 'Cash Account':
                total += item.amount
        return total

    def get_inward(self):
        if not self.lotto_sales_dispenser_amount:
            lotto_sales_dispenser_amount = 0
        else:
            lotto_sales_dispenser_amount = float(self.lotto_sales_dispenser_amount)
        if not self.register_sales_tax:
            register_sales_tax = 0
        else:
            register_sales_tax = float(self.register_sales_tax)
        scratch_off = ScratchOffLatest.objects.filter(date=self.date, company=self.company)
        scratch_off_total = 0
        if scratch_off:
            for scratch in scratch_off:
                scratch_off_total += scratch.grand_total()

        inward_amount = self.get_total_cash_sales() + self.get_total_summary_transfer() + \
                        lotto_sales_dispenser_amount + scratch_off_total + \
                        register_sales_tax - self.get_total_card_sales() - self.get_total_cash_equivalent_sales()
        return inward_amount

    def get_outward(self):
        outward_amount = self.get_total_vendor_payouts() + self.get_total_other_payouts() + self.get_total_deposits()
        return outward_amount

    def get_opening_balance(self):
        day = self.date
        obj = Account.objects.filter(name='Cash Account', company=self.company)[0]
        opening_balance = obj.get_day_opening(day)
        return opening_balance

    def get_closing_balance(self):
        closing_balance = self.get_opening_balance() + self.get_inward() - self.get_outward()
        return closing_balance

    def get_absolute_url(self):
        return '/day/' + str(self.date)

    def get_voucher_no(self):
        return self.voucher_no

    def get_voucher_description(self):
        return ''

    def get_company(self):
        return self.company

    def __str__(self):
        return 'Day Journal at ' + str(self.date)

    class Meta:
        db_table = 'day_journal'
        unique_together = ('voucher_no', 'company')

    def backend_approve(self):
        if self.status == 'Approved':
            pass
        elif self.status == 'Unapproved':
            journal = self
            cash_account = Account.objects.get(name='Cash Account', company=self.company)
            card_account = Account.objects.get(name='Card Account', company=self.company)
            total_amount = 0
            total_tax = 0
            total_sec_tax1 = 0
            for cash_sale in journal.cash_sales.all():
                try:
                    pri_tax_scheme = cash_sale.sales_ledger.tax_detail.all()[0].pri_tax_scheme.percent or 0
                except (IndexError, AttributeError):
                    pri_tax_scheme = 0
                try:
                    sec_tax_scheme1 = cash_sale.sales_ledger.tax_detail.all()[0].sec_tax_scheme_1.percent or 0
                except (IndexError, AttributeError):
                    sec_tax_scheme1 = 0
                pri_tax_amount = cash_sale.amount * zero_for_none(pri_tax_scheme) / 100
                sec_tax_amount1 = cash_sale.amount * zero_for_none(sec_tax_scheme1) / 100
                if zero_for_none(cash_sale.amount) > 0:
                    set_transactions(journal, journal.date,
                                     ['cr', cash_sale.sales_ledger, cash_sale.amount],
                    )
                total_amount += cash_sale.amount
                total_sec_tax1 += sec_tax_amount1
            if journal.lotto_sales_dispenser_amount is None or journal.lotto_sales_dispenser_amount == 0:
                lotto_amount = 0
            else:
                lotto_amount = journal.lotto_sales_dispenser_amount
            total_amount += lotto_amount
            lotto_sales_ledger = Account.objects.get(name='Lotto Sales', company=self.company)
            try:
                lotto_pri_tax_scheme = lotto_sales_ledger.tax_detail.all()[0].pri_tax_scheme.percent
            except (IndexError, AttributeError):
                lotto_pri_tax_scheme = 0
            try:
                lotto_sec_tax_scheme1 = lotto_sales_ledger.tax_detail.all()[0].sec_tax_scheme_1.percent
            except (IndexError, AttributeError):
                lotto_sec_tax_scheme1 = 0
            lotto_pri_tax = lotto_amount * zero_for_none(lotto_pri_tax_scheme) / 100
            lotto_sec_tax1 = lotto_amount * zero_for_none(lotto_sec_tax_scheme1) / 100
            total_sec_tax1 += lotto_sec_tax1
            if zero_for_none(lotto_amount) > 0:
                set_transactions(journal, journal.date,
                                 ['cr', lotto_sales_ledger, lotto_amount],
                )
            scratch_off_total = 0
            for scratch_off in ScratchOffLatest.objects.filter(company=self.company, date=self.date):
                scratch_off_total += scratch_off.grand_total()
            if scratch_off_total == 0:
                scratch_off_total = 0
            if journal.scratch_off_sales_manual:
                scratch_off_total = journal.scratch_off_sales_manual
            total_amount += scratch_off_total
            scratch_off_ledger = Account.objects.get(name='Scratch Off Sales', company=self.company)
            try:
                scratch_off_pri_tax_scheme = scratch_off_ledger.tax_detail.all()[0].pri_tax_scheme.percent
            except (IndexError, AttributeError):
                scratch_off_pri_tax_scheme = 0
            try:
                scratch_off_sec_tax_scheme1 = scratch_off_ledger.tax_detail.all()[0].sec_tax_scheme_1.percent
            except (IndexError, AttributeError):
                scratch_off_sec_tax_scheme1 = 0
            scratch_off_pri_tax = scratch_off_total * zero_for_none(scratch_off_pri_tax_scheme) / 100
            scratch_off_sec_tax1 = scratch_off_total * zero_for_none(scratch_off_sec_tax_scheme1) / 100
            total_sec_tax1 += scratch_off_sec_tax1
            if zero_for_none(scratch_off_total) > 0:
                set_transactions(journal, journal.date,
                                 ['cr', scratch_off_ledger, scratch_off_total],
                )

            actual_sales_tax = zero_for_none(journal.register_sales_tax) - total_sec_tax1
            if zero_for_none(actual_sales_tax) > 0:
                set_transactions(journal, journal.date,
                                 ['cr', Account.objects.get(name='Sales Tax', company=self.company), actual_sales_tax],
                )
            if zero_for_none(total_sec_tax1) > 0:
                set_transactions(journal, journal.date,
                                 ['cr', Account.objects.get(name='Telephone Tax', company=self.company),
                                  total_sec_tax1],
                )

            non_cash = 0
            for card_sale in journal.card_sales.all():
                commission_out = card_sale.commission_out or 0
                net = card_sale.amount - commission_out
                if commission_out > 0:
                    set_transactions(journal, journal.date,
                                     ['dr', Account.objects.get(name='Commission Out', company=self.company),
                                      commission_out], )
                if net > 0:
                    set_transactions(journal, journal.date, ['dr', card_account, net], )
                non_cash += card_sale.amount

            for cash_equivalent_sale in journal.cash_equivalent_sales.all():
                if cash_equivalent_sale.amount > 0:
                    set_transactions(journal, journal.date,
                                     ['dr', cash_equivalent_sale.account, cash_equivalent_sale.amount], )
                non_cash += cash_equivalent_sale.amount
            total_tax = journal.register_sales_tax
            if (total_amount + total_tax + total_sec_tax1 - non_cash) > 0:
                set_transactions(journal, journal.date, ['dr', cash_account, total_amount + total_tax - non_cash], )

            commission_in_account = Account.objects.get(company=self.company, name='Commission In')
            for row in journal.summary_transfer.all():
                if zero_for_none(row.cash) > 0 and zero_for_none(row.commission) > 0:
                    set_transactions(row, journal.date,
                                     ['dr', cash_account, zero_for_none(row.cash)],
                                     ['cr', row.transfer_type, zero_for_none(row.cash) - zero_for_none(row.commission)],
                                     ['cr', commission_in_account, zero_for_none(row.commission)],
                    )
                if zero_for_none(row.cash) > 0 >= zero_for_none(row.commission):
                    set_transactions(row, journal.date,
                                     ['dr', cash_account, zero_for_none(row.cash)],
                                     ['cr', row.transfer_type, zero_for_none(row.cash)],
                    )

            for row in journal.vendor_payout.all():
                if row.type == 'new':
                    if zero_for_none(row.amount) > 0:
                        set_transactions(row, journal.date,
                                         ['dr', row.purchase_ledger, row.amount],
                                         ['cr', row.paid, row.amount],
                        )
                else:
                    if zero_for_none(row.amount) > 0:
                        set_transactions(row, journal.date,
                                         ['dr', row.vendor, row.amount],
                                         ['cr', row.paid, row.amount],
                        )

            for row in journal.vendor_charge.all():
                if zero_for_none(row.amount) > 0:
                    set_transactions(row, journal.date,
                                     ['dr', row.purchase_ledger, row.amount],
                                     ['cr', row.vendor, row.amount],
                    )

            for row in journal.deposits.all():
                if zero_for_none(row.amount) > 0:
                    set_transactions(row, journal.date,
                                     ['dr', row.deposit_in, row.amount],
                                     ['cr', row.deposit_from, row.amount],
                    )

            for row in journal.other_payout.all():
                if zero_for_none(row.amount) > 0:
                    set_transactions(row, journal.date,
                                     ['dr', row.paid_to, row.amount],
                                     ['cr', row.paid, row.amount],
                    )

            for row in journal.summary_inventory.all():
                if row.purchase > 0:
                    InventoryLedger(date=journal.date, company=journal.company, account=row.particular,
                                    in_quantity=row.purchase, in_rate=0, out_quantity=0, out_rate=0,
                                    content_type=ContentType.objects.get(model='dayjournal'),
                                    object_id=journal.id).save()
                elif row.purchase < 0:
                    InventoryLedger(date=journal.date, company=journal.company, account=row.particular,
                                    in_quantity=0, in_rate=0, out_quantity=row.purchase, out_rate=0,
                                    content_type=ContentType.objects.get(model='dayjournal'),
                                    object_id=journal.id).save()
                if row.sales > 0:
                    InventoryLedger(date=journal.date, company=journal.company, account=row.particular,
                                    in_quantity=0, in_rate=0, out_quantity=row.purchase, out_rate=0,
                                    content_type=ContentType.objects.get(model='dayjournal'),
                                    object_id=journal.id).save()
                elif row.sales < 0:
                    InventoryLedger(date=journal.date, company=journal.company, account=row.particular,
                                    in_quantity=row.purchase, in_rate=0, out_quantity=0, out_rate=0,
                                    content_type=ContentType.objects.get(model='dayjournal'),
                                    object_id=journal.id).save()

            for row in journal.inventory_fuel.all():
                if zero_for_none(row.purchase) > 0:
                    InventoryLedger(date=journal.date, company=journal.company, account=row.particular,
                                    in_quantity=zero_for_none(row.purchase), in_rate=0, out_quantity=0, out_rate=0,
                                    content_type=ContentType.objects.get(model='dayjournal'),
                                    object_id=journal.id).save()
                elif zero_for_none(row.purchase) < 0:
                    InventoryLedger(date=journal.date, company=journal.company, account=row.particular,
                                    in_quantity=0, in_rate=0, out_quantity=zero_for_none(row.purchase), out_rate=0,
                                    content_type=ContentType.objects.get(model='dayjournal'),
                                    object_id=journal.id).save()
                if zero_for_none(row.sales) > 0:
                    InventoryLedger(date=journal.date, company=journal.company, account=row.particular,
                                    in_quantity=0, in_rate=0, out_quantity=row.sales, out_rate=0,
                                    content_type=ContentType.objects.get(model='dayjournal'),
                                    object_id=journal.id).save()
                elif zero_for_none(row.sales) < 0:
                    InventoryLedger(date=journal.date, company=journal.company, account=row.particular,
                                    in_quantity=zero_for_none(row.sales), in_rate=0, out_quantity=0, out_rate=0,
                                    content_type=ContentType.objects.get(model='dayjournal'),
                                    object_id=journal.id).save()


            journal.status = 'Approved'
            journal.save()
        return journal.status

    def backend_unapprove(self):
        if self.status == 'Approved':
            entries = JournalEntry.objects.filter(content_type__app_label='dayjournal', date=self.date)

            for entry in entries:
                entry.delete()

            inventory_entries = InventoryLedger.objects.filter(
                content_type=ContentType.objects.get(model='dayjournal'), object_id=self.id)
            for each in inventory_entries:
                each.delete()

            self.status = 'Unapproved'
            self.save()
        return self.status


class Deposits(models.Model):
    sn = models.IntegerField()
    deposit_in = models.ForeignKey(Account, related_name='deposit_in')
    amount = models.FloatField(default=0)
    deposit_from = models.ForeignKey(Account, related_name='deposit_from')
    remarks = models.TextField(blank=True, null=True)
    day_journal = models.ForeignKey(DayJournal, related_name='deposits')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#deposits'

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return self.remarks

    def get_company(self):
        return self.day_journal.company


class CashSales(models.Model):
    sn = models.IntegerField()
    sales_ledger = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_sales')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#cash-sales'

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return ''

    def get_company(self):
        return self.day_journal.company


class SummaryTransfer(models.Model):
    sn = models.IntegerField()
    transfer_type = models.ForeignKey(Account)
    cash = models.FloatField(blank=True, null=True)
    commission = models.FloatField(blank=True, null=True, default=0)
    day_journal = models.ForeignKey(DayJournal, related_name='summary_transfer')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#summary-transfer'

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return ''

    def get_company(self):
        return self.day_journal.company


class CardSales(models.Model):
    amount = models.FloatField()
    commission_out = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='card_sales')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#card-sales'

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return ''

    def get_company(self):
        return self.day_journal.company


class CashEquivalentSales(models.Model):
    sn = models.IntegerField()
    account = models.ForeignKey(Account)
    amount = models.FloatField()
    day_journal = models.ForeignKey(DayJournal, related_name='cash_equivalent_sales')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#cash-equivalent-sales'

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return ''

    def get_company(self):
        return self.day_journal.company


class SummaryInventory(models.Model):
    sn = models.IntegerField()
    particular = models.ForeignKey(InventoryAccount)
    purchase = models.IntegerField()
    sales = models.IntegerField()
    actual = models.IntegerField()
    day_journal = models.ForeignKey(DayJournal, related_name='summary_inventory')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#summary-inventory'

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return ''

    def get_company(self):
        return self.day_journal.company


class InventoryFuel(models.Model):
    sn = models.IntegerField()
    particular = models.ForeignKey(InventoryAccount)
    purchase = models.IntegerField()
    sales = models.IntegerField()
    actual = models.IntegerField()
    day_journal = models.ForeignKey(DayJournal, related_name='inventory_fuel')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#inventory-fuel'

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return ''

    def get_company(self):
        return self.day_journal.company


# Name changed to Scratch Off
class LottoDetail(models.Model):
    sn = models.IntegerField()
    rate = models.FloatField()
    pack_count = models.IntegerField(default=1)
    day_open = models.IntegerField()
    day_close = models.IntegerField()
    addition = models.IntegerField()
    day_journal = models.ForeignKey(DayJournal, related_name='lotto_detail')

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#lotto-detail'

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return ''

    def get_company(self):
        return self.day_journal.company


class SalesAttachment(models.Model):
    attachment = models.FileField(upload_to='day_sales_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    day_journal = models.ForeignKey(DayJournal, related_name='sales_attachments')

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_company(self):
        return self.day_journal.company


class PurchaseAttachment(models.Model):
    attachment = models.FileField(upload_to='day_purchase_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    day_journal = models.ForeignKey(DayJournal, related_name='purchase_attachments')

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_company(self):
        return self.day_journal.company


class BankAttachment(models.Model):
    attachment = models.FileField(upload_to='day_bank_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    day_journal = models.ForeignKey(DayJournal, related_name='bank_attachments')

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_company(self):
        return self.day_journal.company


class OtherAttachment(models.Model):
    attachment = models.FileField(upload_to='day_other_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    day_journal = models.ForeignKey(DayJournal, related_name='other_attachments')

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_company(self):
        return self.day_journal.company


class VendorPayout(models.Model):
    sn = models.IntegerField()
    vendor = models.ForeignKey(Account, related_name="vendor_payouts")
    amount = models.FloatField()
    purchase_ledger = models.ForeignKey(Account, related_name='payouts', null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    paid = models.ForeignKey(Account)
    choices = [('new', 'New Purchase'), ('old', 'Old Bill Payment'), ('settlement', 'Account Settlement'),
               ('payment', 'Advance Payment')]
    type = models.CharField(max_length=10, choices=choices, default='new')
    day_journal = models.ForeignKey(DayJournal, related_name='vendor_payout')

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return self.remarks

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#vendor-payout'

    def get_company(self):
        return self.day_journal.company


class OtherPayout(models.Model):
    sn = models.IntegerField()
    paid_to = models.ForeignKey(Account, related_name='paid_for')
    amount = models.FloatField()
    remarks = models.TextField(null=True, blank=True)
    paid = models.ForeignKey(Account)
    day_journal = models.ForeignKey(DayJournal, related_name='other_payout')

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return self.remarks

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#other-payout'

    def get_company(self):
        return self.day_journal.company


class VendorCharge(models.Model):
    sn = models.IntegerField()
    vendor = models.ForeignKey(Account, related_name="vendor_charge")
    amount = models.FloatField()
    purchase_ledger = models.ForeignKey(Account, related_name='charges', null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    day_journal = models.ForeignKey(DayJournal, related_name='vendor_charge')

    def get_voucher_no(self):
        return self.day_journal.get_voucher_no()

    def get_voucher_description(self):
        return self.remarks

    def get_absolute_url(self):
        return '/day/' + str(self.day_journal.date) + '/#vendor-charge/'

    def get_company(self):
        return self.day_journal.company


# ###NEW SCRATCH-OFF MODELS
class ScratchOffLatest(models.Model):
    date = models.DateField()
    in_time = models.CharField(null=False, blank=False, max_length=10)
    out_time = models.CharField(null=False, blank=False, max_length=10)
    company = models.ForeignKey(Company)
    user = models.ForeignKey(User, null=True, blank=True, related_name='scratch_off_logs')

    def grand_total(self):
        grand_total = 0
        for each in self.rows.all():
            grand_total = grand_total + each.total()
        return grand_total

    def get_absolute_url(self):
        return '/day/scratch-off-latest/' + str(self.id)


class ScratchOffLatestRow(models.Model):
    sn = models.IntegerField()
    rate = models.FloatField(null=False, blank=False)
    packet_count = models.FloatField()
    in_count = models.FloatField()
    out_count = models.FloatField()
    addition = models.FloatField(null=True, blank=True)
    scratch_off = models.ForeignKey(ScratchOffLatest, related_name='rows')

    def total(self):
        total = 0
        total = total + ((zero_for_none(self.out_count) - zero_for_none(self.in_count)) + zero_for_none(
            self.addition)) * zero_for_none(self.rate)
        return total


watson.register(ScratchOffLatest, fields = ('date', 'user'))
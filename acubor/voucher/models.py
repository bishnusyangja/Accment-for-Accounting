from django.db import models

from lib import get_next_voucher_no
from inventory.models import Item
from ledger.models import Account, Party
from ledger.models import TaxScheme
from users.models import Company
import watson
from ledger.models import set_transactions, JournalEntry, Transaction
from django.contrib.contenttypes.models import ContentType


class Invoice(models.Model):
    tax_choices = [('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ('no', 'No Tax')]
    party = models.ForeignKey(Account, verbose_name=u'To', null=True, blank=True)
    date = models.DateField(null=True, blank=True, verbose_name='Invoice Date')
    due_date = models.DateField(null=True, blank=True)
    voucher_no = models.IntegerField(verbose_name='Invoice No.')
    reference = models.CharField(max_length=100, null=True, blank=True)
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive', null=True, blank=True)
    company = models.ForeignKey(Company)
    statuses = [('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')
    pending_amount = models.FloatField(null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'invoice'

    def get_voucher_no(self):
        return self.voucher_no

    def get_absolute_url(self):
        return '/voucher/invoice/' + str(self.id) + '/'

    def get_voucher_description(self):
        return self.description

    def get_company(self):
        return self.company

    def backend_approve(self):
        if self.status == 'Unapproved':
            ctype = ContentType.objects.get_for_model(self)
            journal_entry = JournalEntry(date=self.date, content_type=ctype, object_id=self.id)
            journal_entry.save()
            for row in self.particulars.all():
                try:
                    if row.tax_scheme.collection_ledger is None:
                        tax_ledger = Account.objects.get(name='Sales Tax', company=self.company)
                    else:
                        tax_ledger = row.tax_scheme.collection_ledger
                except:
                    tax_ledger = None
                if row.tax_scheme:
                    tax_percent = row.tax_scheme.percent
                else:
                    tax_percent = 0
                wo_discount = row.quantity * row.unit_price
                amt = wo_discount - ((row.discount * wo_discount) / 100)
                if self.tax == 'exclusive':
                    tax_amount = amt * (tax_percent / 100)
                    net_amount = amt
                elif self.tax == 'inclusive':
                    tax_amount = amt * (tax_percent / (100 + tax_percent))
                    net_amount = amt - tax_amount
                elif self.tax == 'no':
                    tax_amount = 0
                    net_amount = amt
                sales_account = row.account
                transaction = Transaction(account=sales_account, dr_amount=0, cr_amount=net_amount,
                                          company=self.company, journal_entry=journal_entry)
                transaction.save()
                if tax_amount > 0 and tax_ledger is not None:
                    transaction = Transaction(account=tax_ledger, dr_amount=0, cr_amount=tax_amount,
                                          company=self.company, journal_entry=journal_entry)
                    transaction.save()
            transaction = Transaction(account=self.party, dr_amount=self.total_amount, cr_amount=0,
                                          company=self.company, journal_entry=journal_entry)
            transaction.save()
            self.status = 'Approved'
            self.save()
        return self.status

    def backend_unapprove(self):
        if self.status == 'Approved':
            ctype = ContentType.objects.get_for_model(self)
            for entry in JournalEntry.objects.filter(content_type=ctype, object_id=self.id):
                entry.delete()
            self.status = 'Unapproved'
            self.save()
        return self.status

    def __init__(self, *args, **kwargs):
        super(Invoice, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(Invoice, self.company)

    def __unicode__(self):
        return "Invoice at %s" % self.date


class InvoiceParticular(models.Model):
    sn = models.IntegerField()
    description = models.TextField(null=True)
    quantity = models.FloatField(default=1)
    unit_price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    account = models.ForeignKey(Account, blank=True, null=True)
    tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', blank=True, null=True)
    invoice = models.ForeignKey(Invoice, related_name='particulars')

    def get_absolute_url(self):
        return self.invoice.get_absolute_url()

    def get_voucher_no(self):
        return self.invoice.voucher_no

    def get_voucher_description(self):
        return self.invoice.description

    def get_company(self):
        return self.invoice.company

    class Meta:
        db_table = 'invoice_particular'


class PurchaseVoucher(models.Model):
    voucher_no = models.IntegerField(verbose_name='Voucher No.')
    party = models.ForeignKey(Account, verbose_name=u'From', null=True)
    date = models.DateField(null=True)
    due_date = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True, verbose_name='Reference No.')
    tax_choices = [('inclusive', 'Tax Inclusive'), ('exclusive', 'Tax Exclusive'), ('no', 'No Tax')]
    tax = models.CharField(max_length=10, choices=tax_choices, default='inclusive')
    attachment = models.FileField(upload_to='purchase_vouchers/%Y/%m/%d', blank=True, null=True)
    company = models.ForeignKey(Company)
    pending_amount = models.FloatField(null=True)
    total_amount = models.FloatField(null=True)
    description = models.TextField(null=True, blank=True)
    statuses = [('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(PurchaseVoucher, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(PurchaseVoucher, self.company)

    def get_voucher_no(self):
        return self.voucher_no

    def get_voucher_description(self):
        return self.description

    def get_company(self):
        return self.company

    def get_absolute_url(self):
        return '/voucher/purchase-voucher/' + str(self.id) + '/'

    def grand_total(self):
        total = 0
        for item in self.particulars.all():
            amt = (item.unit_price * item.quantity)*(1 - item.discount/100.0)
            tot = amt*(1+item.tax_scheme.percent/100.0) if item.tax_scheme else amt
            total += tot
        return total

    def backend_approve(self):
        if self.status == 'Unapproved':
            ctype = ContentType.objects.get_for_model(self)
            journal_entry = JournalEntry(date=self.date, content_type=ctype, object_id=self.id)
            journal_entry.save()
            for row in self.particulars.all():
                wo_discount = row.quantity * row.unit_price
                amt = wo_discount - ((row.discount * wo_discount) / 100) if row.discount else wo_discount
                if row.tax_scheme:
                    if str(row.tax_scheme.name) == 'No Tax':
                        tax_ledger = None
                    elif row.tax_scheme.collection_ledger is None:
                        tax_ledger = Account.objects.get(name='No Tax', company=self.company)
                    else:
                        tax_ledger = row.tax_scheme.collection_ledger
                    tax_percent = row.tax_scheme.percent
                    tax_amount = amt * (tax_percent / 100)
                    if tax_ledger is not None:
                        transaction = Transaction(account=tax_ledger, cr_amount=0, dr_amount=tax_amount,
                                          company=self.company, journal_entry=journal_entry)
                        transaction.save()
                net_amount = amt
                sales_account = row.account
                transaction = Transaction(account=sales_account, cr_amount=0, dr_amount=net_amount,
                                          company=self.company, journal_entry=journal_entry)
                transaction.save()
            transaction = Transaction(account=self.party, cr_amount=self.grand_total(), dr_amount=0,
                                          company=self.company, journal_entry=journal_entry)
            transaction.save()
            self.status = 'Approved'
            self.save()
        return self.status

    def backend_unapprove(self):
        if self.status == 'Approved':
            ctype = ContentType.objects.get_for_model(self)
            for entry in JournalEntry.objects.filter(content_type=ctype, object_id=self.id):
                entry.delete()
            self.status = 'Unapproved'
            self.save()
        return self.status

    def __unicode__(self):
        return "Purchase Voucher at %s" % self.date


class PurchaseParticular(models.Model):
    sn = models.IntegerField()
    description = models.TextField(null=True)
    quantity = models.FloatField(default=1)
    unit_price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    account = models.ForeignKey(Account, blank=True, null=True)
    tax_scheme = models.ForeignKey(TaxScheme, verbose_name=u'Tax Rate', blank=True, null=True)
    purchase_voucher = models.ForeignKey(PurchaseVoucher, related_name='particulars')

    def get_absolute_url(self):
        return self.purchase_voucher.get_absolute_url()

    def get_voucher_no(self):
        return self.purchase_voucher.get_voucher_no()

    def get_voucher_description(self):
        return self.purchase_voucher.get_voucher_description()

    def get_company(self):
        return self.purchase_voucher.company

    class Meta:
        db_table = 'purchase_particular'


class JournalVoucher(models.Model):
    voucher_no = models.IntegerField()
    date = models.DateField()
    company = models.ForeignKey(Company)
    narration = models.TextField(null=True)
    attachment = models.FileField(upload_to='journal_voucher/%Y/%m/%d', blank=True, null=True)
    statuses = [('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def get_voucher_no(self):
        return self.voucher_no

    def get_voucher_description(self):
        return self.narration

    def get_company(self):
        return self.company

    def backend_approve(self):
        if self.status == 'Approved':
            pass
        elif self.status == 'Unapproved':
            voucher = self
            ctype = ContentType.objects.get_for_model(voucher)
            journal_entry = JournalEntry(date=voucher.date, content_type=ctype, object_id=voucher.id)
            journal_entry.save()
            for row in voucher.rows.all():
                if row.type == 'Dr':
                    transaction = Transaction(account=row.account, cr_amount=0, dr_amount=row.dr_amount,
                                                company=self.company, journal_entry=journal_entry)
                    transaction.save()
                else:
                    transaction = Transaction(account=row.account, cr_amount=row.amount, dr_amount=0,
                                                company=self.company, journal_entry=journal_entry)
                    transaction.save()
            voucher.status = 'Approved'
            voucher.save()

    def backend_unapprove(self):
        if self.status == 'Approved':
            obj = self
            ctype = ContentType.objects.get(model='journalvoucher')
            entries = JournalEntry.objects.filter(content_type=ctype, object_id=obj.id)
            for entry in entries:
                entry.delete()
            self.status = 'Unapproved'
            self.save()

    def __init__(self, *args, **kwargs):
        super(JournalVoucher, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(JournalVoucher, self.company)

    def __unicode__(self):
        return "Journal Voucher at %s" % self.date

    def get_absolute_url(self):
        return '/voucher/journal/' + str(self.id)


class JournalVoucherRow(models.Model):
    types = [('Dr', 'Dr'), ('Cr', 'Dr')]
    type = models.CharField(choices=types, default='Dr', max_length=2)
    account = models.ForeignKey(Account, related_name='account_rows')
    description = models.TextField(null=True, blank=True)
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    journal_voucher = models.ForeignKey(JournalVoucher, related_name='rows')

    def get_absolute_url(self):
        return '/voucher/journal/' + str(self.journal_voucher_id)

    def get_voucher_no(self):
        return self.journal_voucher.voucher_no

    def get_voucher_description(self):
        return self.journal_voucher.narration

    def get_company(self):
        return self.journal_voucher.company

    def __str__(self):
        return ""


class CashReceipt(models.Model):
    voucher_no = models.IntegerField()
    date = models.DateField()
    cash_account = models.ForeignKey(Account, related_name='cash_receipt', null=True)
    attachment = models.FileField(upload_to='cash_receipt/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(CashReceipt, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(CashReceipt, self.company)

    def get_absolute_url(self):
        return '/voucher/cash-receipt/' + str(self.id)

    def get_voucher_no(self):
        return self.voucher_no

    def get_voucher_description(self):
        return self.narration

    def get_company(self):
        return self.company

    def backend_approve(self):
        if self.status == 'Approved':
            pass
        elif self.status == 'Unapproved':
            voucher = self
            cash_account = self.cash_account
            ctype = ContentType.objects.get_for_model(voucher)
            journal_entry = JournalEntry(date=voucher.date, content_type=ctype, object_id=voucher.id)
            journal_entry.save()
            for row in voucher.rows.all():
                transaction = Transaction(account=row.from_account, cr_amount=row.amount, dr_amount=0,
                                                company=self.company, journal_entry=journal_entry)
                transaction.save()
                transaction = Transaction(account=cash_account, cr_amount=0, dr_amount=row.amount,
                                                company=self.company, journal_entry=journal_entry)
                transaction.save()
            voucher.status = 'Approved'
            voucher.save()

    def backend_unapprove(self):
        if self.status == 'Approved':
            obj = self
            obj_rows = self.rows.all()
            ctype = ContentType.objects.get(model='cashreceipt')
            entries = JournalEntry.objects.filter(content_type=ctype, object_id=self.id)
            for entry in entries:
                entry.delete()
            ctype = ContentType.objects.get(model='cashreceiptrow')
            for item in obj_rows:
                entries = JournalEntry.objects.filter(content_type=ctype, object_id=item.id)
                for entry in entries:
                    entry.delete()
            obj.status = 'Unapproved'
            obj.save()

    def __unicode__(self):
        return "Cash Receipt at %s" % self.date


class CashReceiptRow(models.Model):
    sn = models.CharField(max_length=50, blank=True, null=True)
    from_account = models.ForeignKey(Account, null=True)
    amount = models.FloatField(default=0)
    reference_no = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    cash_receipt = models.ForeignKey(CashReceipt, related_name='rows')

    def get_absolute_url(self):
        return '/voucher/cash-receipt/' + str(self.cash_receipt.id)

    def get_voucher_no(self):
        return self.cash_receipt.voucher_no

    def get_voucher_description(self):
        return self.description

    def get_company(self):
        return self.cash_receipt.company


class CashPayment(models.Model):
    voucher_no = models.IntegerField()
    date = models.DateField()
    cash_account = models.ForeignKey(Account, related_name='cash_payment', null=True)
    attachment = models.FileField(upload_to='cash_payment/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(CashPayment, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(CashPayment, self.company)

    def get_absolute_url(self):
        return '/voucher/cash-payment/' + str(self.id)

    def get_voucher_no(self):
        return self.voucher_no

    def get_voucher_description(self):
        return self.narration

    def get_company(self):
        return self.company

    def backend_approve(self):
        if self.status == 'Approved':
            pass
        elif self.status == 'Unapproved':
            voucher = self
            cash_account = self.cash_account
            ctype = ContentType.objects.get_for_model(voucher)
            journal_entry = JournalEntry(date=voucher.date, content_type=ctype, object_id=voucher.id)
            journal_entry.save()
            for row in voucher.rows.all():
                transaction = Transaction(account=row.to_account, dr_amount=row.amount, cr_amount=0,
                                                company=self.company, journal_entry=journal_entry)
                transaction.save()
                transaction = Transaction(account=cash_account, dr_amount=0, cr_amount=row.amount,
                                                company=self.company, journal_entry=journal_entry)
                transaction.save()

            voucher.status = 'Approved'
            voucher.save()

    def backend_unapprove(self):
        if self.status == 'Approved':
            obj = self
            obj_rows = self.rows.all()
            ctype = ContentType.objects.get(model='cashpayment')
            entries = JournalEntry.objects.filter(content_type=ctype, object_id=self.id)
            for entry in entries:
                entry.delete()
            ctype = ContentType.objects.get(model='cashpaymentrow')
            for item in obj_rows:
                entries = JournalEntry.objects.filter(content_type=ctype, object_id=item.id)
                for entry in entries:
                    entry.delete()
            obj.status = 'Unapproved'
            obj.save()

    def __unicode__(self):
        return "Cash Payment at %s" % self.date


class CashPaymentRow(models.Model):
    sn = models.CharField(max_length=50, blank=True, null=True)
    to_account = models.ForeignKey(Account, null=True)
    amount = models.FloatField(default=0)
    reference_no = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    cash_payment = models.ForeignKey(CashPayment, related_name='rows')

    def get_absolute_url(self):
        return '/voucher/cash-payment/' + str(self.cash_payment.id)

    def get_voucher_no(self):
        return self.cash_payment.voucher_no

    def get_voucher_description(self):
        return self.description

    def get_company(self):
        return self.cash_payment.company


class FixedAsset(models.Model):
    from_account = models.ForeignKey(Account, null=True)
    voucher_no = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, null=True)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def get_voucher_description(self):
        return self.description

    def __init__(self, *args, **kwargs):
        super(FixedAsset, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(FixedAsset, self.company)

    def get_absolute_url(self):
        return '/voucher/fixed-asset/' + str(self.id)

    def get_voucher_no(self):
        return self.voucher_no

    def get_company(self):
        return self.company

    def backend_approve(self):
        # for row in voucher.rows.all():
        #     set_transactions(row, voucher.date,
        #                      ['dr', row.asset_ledger, row.amount],
        #                      ['cr', voucher.from_account, row.amount])
        # voucher.status = 'Approved'
        # voucher.save()
        if self.status == 'Approved':
            pass
        elif self.status == 'Unapproved':
            voucher = self
            ctype = ContentType.objects.get_for_model(voucher)
            for row in voucher.rows.all():
                journal_entry = JournalEntry(date=voucher.date, content_type=ctype, object_id=voucher.id)
                journal_entry.save()

                transaction = Transaction(account=voucher.from_account, cr_amount=row.amount, dr_amount=0,
                                                company=self.company, journal_entry=journal_entry)
                transaction.save()

                transaction = Transaction(account=row.asset_ledger, cr_amount=0, dr_amount=row.amount,
                                                company=self.company, journal_entry=journal_entry)
                transaction.save()

            voucher.status = 'Approved'
            voucher.save()

    def backend_unapprove(self):
        ctype = ContentType.objects.get(model='fixedassetrow')
        entries = JournalEntry.objects.filter(content_type=ctype, object_id=self.id)
        for entry in entries:
            entry.delete()
        self.status = 'Unapproved'
        self.save()
        return self.status


class FixedAssetRow(models.Model):
    asset_ledger = models.ForeignKey(Account, null=True)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField(default=0)
    fixed_asset = models.ForeignKey(FixedAsset, related_name='rows')

    def get_voucher_description(self):
        return self.description


    def get_absolute_url(self):
        return '/voucher/fixed-asset/' + str(self.fixed_asset.id)

    def get_voucher_no(self):
        return self.fixed_asset.voucher_no

    def get_company(self):
        return self.fixed_asset.company


class AdditionalDetail(models.Model):
    assets_code = models.CharField(max_length=100, null=True, blank=True)
    assets_type = models.CharField(max_length=100, null=True, blank=True)
    vendor_name = models.CharField(max_length=100, null=True, blank=True)
    vendor_address = models.CharField(max_length=254, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    useful_life = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    warranty_period = models.CharField(max_length=100, null=True, blank=True)
    maintenance = models.CharField(max_length=100, null=True, blank=True)
    fixed_asset = models.ForeignKey(FixedAsset, related_name='additional_details')

# REGISTER WATSON
watson.register(JournalVoucher, fields=('narration', 'voucher_no'))
watson.register(JournalVoucherRow, fields=('description', 'account', 'dr_amount', 'cr_amount'))
watson.register(CashReceipt, fields=('cash_account', 'narration'))
watson.register(CashReceiptRow, fields=('from_account', 'reference_no', 'amount', 'description'))
watson.register(CashPayment, fields=('cash_account', 'narration'))
watson.register(Invoice, fields=('party', 'description', 'total_amount', 'date'))
watson.register(InvoiceParticular, fields=('description',))

watson.register(PurchaseVoucher, fields=('party', 'description', 'date'))
watson.register(PurchaseParticular, fields=('description', 'unit_price', 'account'))

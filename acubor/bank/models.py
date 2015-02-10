from django.db import models
from ledger.models import Account, JournalEntry, Transaction
from users.models import Company
from lib import get_next_voucher_no
import watson
from django.contrib.contenttypes.models import ContentType


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=254)
    ac_no = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=254, blank=True, null=True)
    account = models.OneToOneField(Account)
    company = models.ForeignKey(Company)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = Account(code=self.ac_no[-10:], name=self.bank_name + ' Account (' + str(self.ac_no) + ' )')
            account.company = self.company
            account.add_category('Bank Account')
            account.save()
            self.account = account
        super(BankAccount, self).save(*args, **kwargs)

    def __str__(self):
        return self.bank_name + ' Account (' + str(self.ac_no) + ' )'

    def get_company(self):
        return self.company


class BankDeposit(models.Model):
    voucher_no = models.IntegerField()
    date = models.DateField()
    bank_account = models.ForeignKey(Account, related_name='bank_deposit')
    attachment = models.FileField(upload_to='bank_deposit/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(BankDeposit, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(BankDeposit, self.company)

    def get_voucher_no(self):
        return self.voucher_no

    def get_voucher_description(self):
        return self.narration

    def get_absolute_url(self):
        return '/bank/bank-deposit/update/' + str(self.id)

    def get_company(self):
        return self.company

    def backend_approve(self):
        if self.status == 'Approved':
            pass
        elif self.status == 'Unapproved':
            voucher = self
            bank_account = self.bank_account
            ctype = ContentType.objects.get_for_model(voucher)
            journal_entry = JournalEntry(date=voucher.date, content_type=ctype, object_id=voucher.id)
            journal_entry.save()
            for row in voucher.rows.all():
                transaction = Transaction(account=row.from_account, cr_amount=row.amount, dr_amount=0,
                                                company=self.company, journal_entry=journal_entry)
                transaction.save()
                transaction = Transaction(account=bank_account, cr_amount=0, dr_amount=row.amount,
                                                company=self.company, journal_entry=journal_entry)
                transaction.save()
            voucher.status = 'Approved'
            voucher.save()

    def backend_unapprove(self):
        if self.status == 'Approved':
            obj = self
            obj_rows = self.rows.all()
            ctype = ContentType.objects.get(model='bankdepositrow')
            for item in obj_rows:
                entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
                for entry in entries:
                    entry.delete()
            obj.status='Unapproved'
            obj.save()

    def __unicode__(self):
        return "Bank Deposit at %s" % self.date


class BankDepositRow(models.Model):
    sn = models.CharField(max_length=50, blank=True, null=True)
    from_account = models.ForeignKey(Account)
    amount = models.FloatField()
    reference_no = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    bank_deposit = models.ForeignKey(BankDeposit, related_name='rows')

    def get_voucher_no(self):
        return self.bank_deposit.voucher_no

    def get_voucher_description(self):
        return self.description

    def get_absolute_url(self):
        return self.bank_deposit.get_absolute_url()

    def get_company(self):
        return self.bank_deposit.company


class BankPayment(models.Model):
    voucher_no = models.IntegerField()
    date = models.DateField()
    bank_account = models.ForeignKey(Account, related_name='bank_payment')
    attachment = models.FileField(upload_to='bank_payment/%Y/%m/%d', blank=True, null=True)
    narration = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __init__(self, *args, **kwargs):
        super(BankPayment, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(BankPayment, self.company)

    def get_voucher_no(self):
        return self.voucher_no

    def get_voucher_description(self):
        return self.narration

    def get_absolute_url(self):
        return '/bank/bank-payment/update/' + str(self.id)

    def get_company(self):
        return self.company

    def backend_approve(self):
        if self.status == 'Approved':
            pass
        elif self.status == 'Unapproved':
            voucher = self
            bank_account = self.bank_account
            ctype = ContentType.objects.get_for_model(voucher)
            journal_entry = JournalEntry(date=voucher.date, content_type=ctype, object_id=voucher.id)
            journal_entry.save()
            for row in voucher.rows.all():
                transaction = Transaction(account=row.to_account, cr_amount=row.amount, dr_amount=0,
                                                company=self.company, journal_entry=journal_entry)
                transaction.save()
                transaction = Transaction(account=bank_account, cr_amount=0, dr_amount=row.amount,
                                          company=self.company, journal_entry=journal_entry)
                transaction.save()
            voucher.status = 'Approved'
            voucher.save()

    def backend_unapprove(self):
        if self.status == 'Approved':
            obj = self
            obj_rows = self.rows.all()
            ctype = ContentType.objects.get(model='bankpaymentrow')
            for item in obj_rows:
                entries = JournalEntry.objects.filter(content_type=ctype,object_id=item.id)
                for entry in entries:
                    entry.delete()
            obj.status = 'Unapproved'
            obj.save()

    def __unicode__(self):
        return "Bank Payment at %s" % self.date


class BankPaymentRow(models.Model):
    sn = models.CharField(max_length=50, blank=True, null=True)
    to_account = models.ForeignKey(Account)
    amount = models.FloatField()
    reference_no = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    bank_payment = models.ForeignKey(BankPayment, related_name='rows')

    def get_voucher_no(self):
        return self.bank_payment.voucher_no

    def get_voucher_description(self):
        return self.description

    def get_absolute_url(self):
        return self.bank_payment.get_absolute_url()

    def get_company(self):
        return self.bank_payment.company

watson.register(BankDeposit, fields=('narration','bank_account'))
watson.register(BankPayment, fields=('narration','bank_account'))
watson.register(BankDepositRow, fields=('from_account','description','reference_no','amount'))
watson.register(BankPaymentRow, fields=('to_account','description','reference_no','amount'))

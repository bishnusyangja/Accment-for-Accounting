import datetime

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.db.models import F, Sum
from django.contrib.contenttypes import generic
from django.core.exceptions import ObjectDoesNotExist

from users.models import Company
from lib import zero_for_none, none_for_zero

import watson


class Category(MPTTModel):
    name = models.CharField(max_length=50, verbose_name="Name *")
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    company = models.ForeignKey(Company)
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/category/' + str(self.id)

    def get_company(self):
        return self.company

    class Meta:
        db_table = 'ledger_category'
        verbose_name_plural = u'Categories'
        unique_together = (('company', 'name'),)

    # def get_my_children(self):
    # return Category.objects.filter(parent=self)

    #get the total dr amount for specified year of  month for a category
    def get_total_dr(self, year, month):
        total = 0
        if self.accounts.all():
            for account in self.accounts.all():
                total += account.get_month_dr(year, month)
        if self.get_children():
            for cat in self.get_children():
                total += cat.get_total_dr(year, month)
        return total

    #get the total cr amount for specified year of  month for a category
    def get_total_cr(self, year, month):
        total = 0
        if self.accounts.all():
            for account in self.accounts.all():
                total += account.get_month_cr(year, month)
        if self.get_children():
            for cat in self.get_children():
                total += cat.get_total_cr(year, month)
        return total

    #get the total dr amount for all of the transaction of the accounts of this category that have been created yet
    def get_cat_tot_dr(self, end):
        total = 0
        if self.accounts.all():
            for account in self.accounts.all():
                total += account.get_dr_amount(end)
        if self.get_children():
            for cat in self.get_children():
                total += cat.get_cat_tot_dr(end)

        return total

    #get the total cr amount for all of the transaction of the accounts of this category that have been created yet
    def get_cat_tot_cr(self, end):
        total = 0
        if self.accounts.all():
            for account in self.accounts.all():
                total += account.get_cr_amount(end)
        if self.get_children():
            for cat in self.get_children():
                total += cat.get_cat_tot_cr(end)
        return total

    #returns all total dr amount of accounts of that category
    def get_acc_total_dr(self, start, end):
        tot = 0
        if self.accounts.all():
            for account in self.accounts.all():
                temp = account.get_dr_amount(end) - account.get_dr_amount(start)
                tot += temp
        return tot

    #returns all total cr amount of accounts of that category
    def get_acc_total_cr(self, start, end):
        tot = 0
        if self.accounts.all():
            for account in self.accounts.all():
                temp = account.get_cr_amount(end) - account.get_cr_amount(start)
                tot += temp
        return tot

    # returns the total dr amount of given category within specified interval
    def get_duration_cat_tot_dr(self, start, end):
        tot = 0
        if self.accounts.all():
            for account in self.accounts.all():
                tot += account.get_dr_amount(end) - account.get_day_opening_dr(start)
        if self.get_children():
            for cat in self.get_children():
                tot += cat.get_duration_cat_tot_dr(start, end)
        return round(tot, 2)

    # returns the total cr amount of given category within specified interval
    def get_duration_cat_tot_cr(self, start, end):
        tot = 0
        if self.accounts.all():
            total = 0
            for account in self.accounts.all():
                total += account.get_cr_amount(end) - account.get_day_opening_cr(start)
            tot += total
        if self.get_children():
            total = 0
            for cat in self.get_children():
                total += cat.get_duration_cat_tot_cr(start, end)
            tot += total
        return round(tot, 2)

    #get the list of recent children dr amount for the given category within the given range
    def get_recent_cat_tot(self, start, end):
        lis = []
        if self.accounts.all():
            for account in self.accounts.all():
                a = {'name': account.name, 'dr': round(account.get_dr_amount(end) - account.get_dr_amount(start), 2),
                     'cr': round(account.get_cr_amount(end) - account.get_cr_amount(start), 2)}
                lis.append(a)
        if self.get_children():
            for cat in self.get_children():
                a = {'name': cat.name, 'dr': cat.get_duration_cat_tot_dr(start, end),
                     'cr': cat.get_duration_cat_tot_cr(start, end)}
                lis.append(a)
        return lis


class Account(models.Model):
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name='Name *')
    company = models.ForeignKey(Company)
    current_dr = models.FloatField(blank=False, null=False, default=0)
    current_cr = models.FloatField(blank=False, null=False, default=0)
    category = models.ForeignKey(Category, related_name='accounts')
    opening_dr = models.FloatField(blank=True, null=True, default=0, verbose_name="Opening Debit Amount")
    opening_cr = models.FloatField(blank=True, null=True, default=0, verbose_name="Opening Credit Amount")
    opening_as_on_date = models.DateField(default=datetime.date.today(), verbose_name="Opening As On Date", blank=True, null=True)
    is_default = models.BooleanField(default=False)
    interest_scheme = models.ForeignKey('InterestScheme', related_name='account', null=True)

    class Meta:
        unique_together = (('company', 'name'), )

    def get_absolute_url(self):
        return '/ledger/' + str(self.id)

    def get_balance(self):
        return zero_for_none(self.get_dr_amount(datetime.date.today())) - zero_for_none(self.get_cr_amount(datetime.date.today()))

    def get_net_opening_balance(self):
        return zero_for_none(self.opening_dr) - zero_for_none(self.opening_cr)

    def get_day_opening_dr(self, before_date):
        if not before_date:
            before_date = datetime.date.today()
        if before_date < self.opening_as_on_date:
            before_date = self.opening_as_on_date
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date)
        total = zero_for_none(self.opening_dr)
        if len(transactions) > 0:
            for each in transactions:
                total = total + zero_for_none(each.dr_amount)
        return total

    def get_day_opening_cr(self, before_date):
        if not before_date:
            before_date = datetime.date.today()
        if before_date < self.opening_as_on_date:
            before_date = self.opening_as_on_date
        transactions = Transaction.objects.filter(account=self, journal_entry__date__lt=before_date)
        total = zero_for_none(self.opening_cr)
        if len(transactions) > 0:
            for each in transactions:
                total = total + zero_for_none(each.cr_amount)
        return total

    def get_day_opening(self, before_date):
        if not before_date:
            before_date = datetime.date.today()
        if before_date < self.opening_as_on_date:
            before_date = self.opening_as_on_date
        return zero_for_none(self.get_day_opening_dr(before_date)) - zero_for_none(self.get_day_opening_cr(before_date))

    def add_category(self, category):
        category_instance, created = Category.objects.get_or_create(name=category, company=self.company)
        self.category = category_instance

    def get_all_categories(self):
        return self.category.get_ancestors(include_self=True)

    categories = property(get_all_categories)

    def get_cr_amount(self, day):
        transactions = Transaction.objects.filter(journal_entry__date__lte=day,
                                                  journal_entry__date__gte=self.opening_as_on_date, account=self)
        total = zero_for_none(self.opening_cr)
        if len(transactions) > 0:
            for each in transactions:
                total = total + zero_for_none(each.cr_amount)
        return total

    def get_dr_amount(self, day):
        transactions = Transaction.objects.filter(journal_entry__date__lte=day,
                                                  journal_entry__date__gte=self.opening_as_on_date, account=self)
        total = zero_for_none(self.opening_dr)
        if len(transactions) > 0:
            for each in transactions:
                total = total + zero_for_none(each.dr_amount)
        return total

    def get_month_cr(self, year, month):
        return zero_for_none(Transaction.objects.filter(account=self, journal_entry__in=JournalEntry \
                                                        .objects.filter(date__year=year, date__month=month).values_list \
            ('id', flat=True)).aggregate(Sum('cr_amount'))['cr_amount__sum'])

    def get_month_dr(self, year, month):
        return zero_for_none(Transaction.objects.filter(account=self, journal_entry__in=JournalEntry \
                                                        .objects.filter(date__year=year, date__month=month).values_list \
            ('id', flat=True)).aggregate(Sum('dr_amount'))['dr_amount__sum'])

    # def get_month_bal(self, year, month):
    # return self.get_month_dr(year, month) - self.get_month_cr(year, month)

    def get_current_dr(self):
        return zero_for_none(self.get_dr_amount(datetime.date.today()))

    def get_current_cr(self):
        return zero_for_none(self.get_cr_amount(datetime.date.today()))

    def get_company(self):
        return self.company

    def get_pri_tax(self):
        if len(self.tax_detail.all()) > 0:
            if hasattr(self.tax_detail.all()[0], 'pri_tax_scheme') and self.tax_detail.all()[0].pri_tax_scheme is not None:
                return self.tax_detail.all()[0].pri_tax_scheme.get_percent()
            else:
                return 0
        else:
            return 0

    def get_sec_tax(self):
        sec_tax = 0
        if len(self.tax_detail.all()) > 0:
            if hasattr(self.tax_detail.all()[0], 'sec_tax_scheme_1') \
                    and self.tax_detail.all()[0].sec_tax_scheme_1 is not None:
                sec_tax = sec_tax + self.tax_detail.all()[0].sec_tax_scheme_1.get_percent()
            if hasattr(self.tax_detail.all()[0], 'sec_tax_scheme_2') \
                    and self.tax_detail.all()[0].sec_tax_scheme_2 is not None:
                sec_tax = sec_tax + self.tax_detail.all()[0].sec_tax_scheme_2.get_percent()
            if hasattr(self.tax_detail.all()[0], 'sec_tax_scheme_3') \
                    and self.tax_detail.all()[0].sec_tax_scheme_3 is not None:
                sec_tax = sec_tax + self.tax_detail.all()[0].sec_tax_scheme_3.get_percent()
        return sec_tax

    def __unicode__(self):
        return self.name


class TaxScheme(models.Model):
    name = models.CharField(max_length=100)
    percent = models.FloatField()
    company = models.ForeignKey(Company)
    is_default = models.BooleanField(default=False)
    collection_ledger = models.ForeignKey(Account, related_name='tax_scheme', null=True)

    def get_absolute_url(self):
        return "/ledger/tax_scheme/" + str(self.id)

    def __str__(self):
        return self.name + ' (' + str(self.percent) + '%)'

    def get_percent(self):
        return zero_for_none(self.percent)


class InterestScheme(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    rate_in_pct = models.FloatField(default=0.0)
    company = models.ForeignKey(Company, null=True)
    collection_ledger = models.ForeignKey(Account, related_name='int_scheme', null=True, blank=True)
    interest_period = models.IntegerField(default=0, null=True, blank=True)


class BankAccountDetail(models.Model):
    account = models.ForeignKey(Account, related_name='bank_detail', null=True, blank=True, verbose_name='bank_name')
    bank_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Bank Name *")
    bank_address = models.CharField(max_length=200, null=True, blank=True)
    contact_no = models.CharField(max_length=20, null=True, blank=True)
    bank_email_address = models.EmailField(null=True, blank=True)
    company = models.ForeignKey(Company, null=True)


class PartyAccountDetail(models.Model):
    account = models.ForeignKey(Account, related_name='party_detail', null=True, blank=True, verbose_name='party_name')
    party_address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Address')
    tin_no = models.CharField(max_length=20, blank=True, null=True, verbose_name='Taxpayer Identification Number')
    party_email_address = models.EmailField(null=True, blank=True, verbose_name='Email Address')
    company = models.ForeignKey(Company, null=True)


class AccountTaxDetail(models.Model):
    account = models.ForeignKey(Account, related_name='tax_detail', null=True, blank=True)
    pri_tax_scheme = models.ForeignKey('TaxScheme', related_name='primary_tax_scheme', null=True, blank=True)
    sec_tax_scheme_1 = models.ForeignKey('TaxScheme', related_name='secondary_tax_scheme_1', null=True, blank=True)
    sec_tax_scheme_2 = models.ForeignKey('TaxScheme', related_name='secondary_tax_scheme_2', null=True, blank=True)
    sec_tax_scheme_3 = models.ForeignKey('TaxScheme', related_name='secondary_tax_scheme_3', null=True, blank=True)
    company = models.ForeignKey(Company, null=True)


class JournalEntry(models.Model):
    date = models.DateField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    source = generic.GenericForeignKey('content_type', 'object_id')
    company = models.ForeignKey(Company, null=True)

    def get_description(self):
        ct = ContentType.objects.get_for_id(self.content_type.id)
        obj = ct.get_object_for_this_type(pk=self.object_id)
        return obj.get_voucher_description()

    def get_company(self):
        ct = ContentType.objects.get_for_id(self.content_type.id)
        try:
            obj = ct.get_object_for_this_type(pk=self.object_id)
        except:
            self.transactions.all().delete()
            self.delete()
            return None
        return obj.get_company()

    def set_company(self):
        if self.get_company():
            self.company = self.get_company()
            self.save()

    def __str__(self):
        return str(self.content_type) + ': ' + str(self.object_id) + ' [' + str(self.date) + ']'

    class Meta:
        verbose_name_plural = u'Journal Entries'


# A model manager
class TransactionManager(models.Manager):
    def total_dr_amount(self, start, end):
        return super(TransactionManager, self).get_query_set().filter(
            journal_entry__in=JournalEntry.objects.filter(date__gte=start, date__lte=end)).values('account').annotate(
            Sum('dr_amount'))

    def total_cr_amount(self, start, end):
        return super(TransactionManager, self).get_query_set().filter(
            journal_entry__in=JournalEntry.objects.filter(date__gte=start, date__lte=end)).values('account').annotate(
            Sum('cr_amount'))


class Transaction(models.Model):
    account = models.ForeignKey(Account)
    dr_amount = models.FloatField(null=True, blank=True)
    cr_amount = models.FloatField(null=True, blank=True)
    current_dr = models.FloatField(null=True, blank=True)
    current_cr = models.FloatField(null=True, blank=True)
    journal_entry = models.ForeignKey(JournalEntry, related_name='transactions')
    company = models.ForeignKey(Company, null=True, blank=True)
    objects = models.Manager()
    total_balance = TransactionManager()

    def get_cr_amount(self):
        transactions_before_date = Transaction.objects.filter(journal_entry__date__lt=self.journal_entry.date, account=self.account)
        transactions_on_date = Transaction.objects.filter(journal_entry__date=self.journal_entry.date, account=self.account, journal_entry__id__lte=self.journal_entry.id)
        transactions = list(transactions_before_date) + list(transactions_on_date)
        total = zero_for_none(self.account.opening_cr)
        if len(transactions) > 0:
            for each in transactions:
                total = total + zero_for_none(each.cr_amount)
        return total

    def get_dr_amount(self):
        transactions_before_date = Transaction.objects.filter(journal_entry__date__lt=self.journal_entry.date, account=self.account)
        transactions_on_date = Transaction.objects.filter(journal_entry__date=self.journal_entry.date, account=self.account, journal_entry__id__lte=self.journal_entry.id)
        transactions = list(transactions_before_date) + list(transactions_on_date)
        total = zero_for_none(self.account.opening_dr)
        if len(transactions) > 0:
            for each in transactions:
                total = total + zero_for_none(each.dr_amount)
        return total


    def get_balance(self):
        return zero_for_none(self.get_dr_amount()) - zero_for_none(self.get_cr_amount())

    def get_description(self):
        return self.journal_entry.get_description()

    def get_company(self):
        return self.company

    def get_source_type(self):
        return self.journal_entry.content_type.name

    def get_voucher_no(self):
        return self.journal_entry.source.get_voucher_no()

    def get_absolute_url(self):
        return self.journal_entry.source.get_absolute_url()

    def get_date(self):
        return self.journal_entry.date

    def get_account(self):
        return self.account

    def __str__(self):
        return str(self.account) + ' [' + str(self.dr_amount) + ' / ' + str(self.cr_amount) + ']'


# journal_entry__in = JournalEntry.objects.filter(date__month = month).values_list('id',flat=True)


class Party(models.Model):
    name = models.CharField(max_length=254)
    address = models.TextField(null=True, blank=True)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    types = [('Customer', 'Customer'), ('Supplier', 'Supplier'), ('Customer/Supplier', 'Customer/Supplier')]
    type = models.CharField(choices=types, max_length=17, default='Customer')
    company = models.ForeignKey(Company)
    customer_account = models.OneToOneField(Account, null=True, related_name='customer_detail')
    supplier_account = models.OneToOneField(Account, null=True, related_name='supplier_detail')
    is_default = models.BooleanField(default=False)

    def get_company(self):
        return self.company

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Party, self).save(*args, **kwargs)
        account = Account(name=self.name, opening_as_on_date=self.company.current_financial_year_started_on)
        account.company = self.company
        if self.type == 'Customer':
            if not self.customer_account:
                account.category = Category.objects.get(name='Customers', company=self.company)
                account.save()
                self.customer_account = account
            if self.supplier_account:
                self.supplier_account.delete()
                self.supplier_account = None
        elif self.type == 'Supplier':
            if not self.supplier_account:
                account.category = Category.objects.get(name='Suppliers', company=self.company)
                account.save()
                self.supplier_account = account
            if self.customer_account:
                self.customer_account.delete()
                self.customer_account = None
        else:
            if not self.customer_account:
                account.name += ' (Receivable)'
                account.category = Category.objects.get(name='Customers', company=self.company)
                account.save()
                self.customer_account = account
            if not self.supplier_account:
                account2 = Account(name=self.name + ' (Payable)', opening_as_on_date=self.company.current_financial_year_started_on)
                account2.company = self.company
                account2.category = Category.objects.get(name='Suppliers', company=self.company)
                account2.save()
                self.supplier_account = account2
        super(Party, self).save(*args, **kwargs)

    class Meta:
        db_table = 'party'


def alter(account, date, dr_difference, cr_difference):
    Transaction.objects.filter(journal_entry__date__gt=date, account=account).update(
        current_dr=none_for_zero(zero_for_none(F('current_dr')) + zero_for_none(dr_difference)),
        current_cr=none_for_zero(zero_for_none(F('current_cr')) + zero_for_none(cr_difference)))


def set_transactions(submodel, date, *args):
    if isinstance(date, unicode):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    journal_entry, created = JournalEntry.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(submodel), object_id=submodel.id,
        defaults={
            'date': date
        })
    for arg in args:
        # transaction = Transaction(account=arg[1], dr_amount=arg[2])
        matches = journal_entry.transactions.filter(account=arg[1])
        if not matches:
            transaction = Transaction()
            transaction.account = arg[1]
            if arg[0] == 'dr':
                transaction.dr_amount = float(zero_for_none(arg[2]))
                transaction.cr_amount = None
                transaction.account.current_dr = zero_for_none(transaction.account.current_dr) + zero_for_none(
                    transaction.dr_amount)
                alter(arg[1], date, float(arg[2]), 0.0)
            if arg[0] == 'cr':
                transaction.cr_amount = float(zero_for_none(arg[2]))
                transaction.dr_amount = None
                transaction.account.current_cr = zero_for_none(transaction.account.current_cr) + zero_for_none(
                    transaction.cr_amount)
                alter(arg[1], date, 0.0, float(arg[2]))
            transaction.current_dr = zero_for_none(transaction.account.get_dr_amount(date)) \
                                     + zero_for_none(transaction.dr_amount)
            transaction.current_cr = zero_for_none(transaction.account.get_cr_amount(date)) \
                                     + zero_for_none(transaction.cr_amount)
            transaction.company = transaction.account.company
        else:
            transaction = matches[0]
            transaction.account = arg[1]

            if arg[0] == 'dr':
                dr_difference = float(arg[2]) - zero_for_none(transaction.dr_amount)
                cr_difference = zero_for_none(transaction.cr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.dr_amount = float(arg[2])
                transaction.cr_amount = None
            else:
                cr_difference = float(arg[2]) - zero_for_none(transaction.cr_amount)
                dr_difference = zero_for_none(transaction.dr_amount) * -1
                alter(arg[1], transaction.journal_entry.date, dr_difference, cr_difference)
                transaction.cr_amount = float(arg[2])
                transaction.dr_amount = None

            transaction.current_dr = zero_for_none(transaction.current_dr) + dr_difference
            transaction.current_cr = zero_for_none(transaction.current_cr) + cr_difference
            transaction.account.current_dr = zero_for_none(transaction.account.current_dr) + dr_difference
            transaction.account.current_cr = zero_for_none(transaction.account.current_cr) + cr_difference
            transaction.company = transaction.account.company
        # print "From set_transaction", transaction.account.company.id
        transaction.account.save()
        journal_entry.transactions.add(transaction)


def delete_rows(rows, model):
    for row in rows:
        if row.get('id'):
            instance = model.objects.get(id=row.get('id'))
            try:
                JournalEntry.objects.get(content_type=ContentType.objects.get_for_model(model),
                                         model_id=instance.id).delete()
            except:
                pass
            instance.delete()


@receiver(pre_delete, sender=Transaction)
def _transaction_delete(sender, instance, **kwargs):
    transaction = instance
    if transaction.dr_amount:
        transaction.account.current_dr -= transaction.dr_amount

    if transaction.cr_amount:
        transaction.account.current_cr -= transaction.cr_amount

    alter(transaction.account, transaction.journal_entry.date, float(zero_for_none(transaction.dr_amount)) * -1,
          float(zero_for_none(transaction.cr_amount)) * -1)

    transaction.account.save()

#WATSON REGISTER
# watson.register(Account, fields=("name","current_dr"))
watson.register(Transaction, fields=('get_description', 'dr_amount', 'get_source_type', 'get_date','get_voucher_no'))
watson.register(Account, fields=('name', 'category'))
# watson.register(JournalEntry, fields=("date","transactions__account__name"))


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
import settings
from django.core.mail import send_mail
import datetime
import smtplib
from email.mime.text import MIMEText


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, full_name='', identifier=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=UserManager.normalize_email(email),
            full_name=full_name,
            identifier=identifier,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, full_name=''):
        """
        Creates and saves a superuser with the given email, full name and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
            full_name=full_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Company(models.Model):
    name = models.CharField(max_length=254)
    location = models.TextField(null=True, blank=True)
    owner_full_name = models.CharField(max_length=254, null=True, blank=True)
    address_line_1 = models.CharField(max_length=100, null=True, blank=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=5, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    type_of_business = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.name

    def is_test_company(self):
        if self.name == 'Test Company Inc' or self.name == 'Test Company':
            return True
        else:
            return False

    class Meta:
        db_table = u'company'
        verbose_name_plural = u'Companies'


from settings import EMAIL_HOST

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=245)
    email = models.EmailField(verbose_name='email address', max_length=254)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    identifier = models.CharField(max_length=245, null=True)
    date_joined = models.DateTimeField(default=datetime.datetime.now(), null=False)
    currently_activated_company = models.ForeignKey(Company, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'email']

    def __unicode__(self):
        return self.username

    def get_short_name(self):
        # The user is identified by username
        return self.username

    def get_full_name(self):
        return self.full_name

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def email_user(self, subject, message, from_email):
        send_ssl_mail(self.email, message, subject)
        # send_mail(subject, message, from_email, [self.email], fail_silently=False)

    def is_superuser(self):
        return self.is_admin

    def get_company_settings(self):
        from core.models import CompanySetting

        return CompanySetting.objects.get(company=self.company)

    objects = UserManager()

    class Meta:
        db_table = u'user'


# class BillingDetails(models.Model):
#     user = models.ForeignKey(User, related_name='billing_details')



def send_ssl_mail(recipient, msg_text, msg_subject):
    # Define to/from
    sender = settings.EMAIL_HOST_USER
    recipient = recipient

    # Create message
    msg = MIMEText(msg_text)
    msg['Subject'] = msg_subject
    msg['From'] = sender
    msg['To'] = recipient

    # Create server object with SSL option
    server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)

    # Perform operations via server
    server.login(sender, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()


def create_default(company, type_of_business, other_params):
    from ledger.models import Account, Category, AccountTaxDetail

    store_specific_accounts = False
    gas_station_specific = False
    if type_of_business in ['Convenience Store', 'Gas Station and Store', ]:
        store_specific_accounts = True
    if type_of_business in ['Gas Station and Store', 'Gas Station', ]:
        gas_station_specific = True

    equity = Category(name='Equity', company=company)
    equity.save()
    Account(name='Paid in Capital', category=equity, company=company).save()
    Account(name='Drawings', category=equity, company=company).save()
    retained_earnings = Category(name='Retained Earning', parent=equity, company=company)
    retained_earnings.save()
    Account(name='Opening', category=retained_earnings, company=company).save()
    Account(name='Profit/Loss', category=retained_earnings, company=company).save()

    liabilities = Category(name='Liabilities', company=company)
    liabilities.save()
    non_current_liabilities = Category(name='Non Current Liabilities', parent=liabilities, company=company)
    non_current_liabilities.save()
    current_liabilities = Category(name='Current Liabilities', parent=liabilities, company=company)
    current_liabilities.save()
    account_payables = Category(name='Account Payables', parent=current_liabilities, company=company)
    account_payables.save()
    Category(name='Suppliers', parent=account_payables, company=company).save()
    secured_loans = Category(name='Secured Loans', parent=current_liabilities, company=company)
    secured_loans.save()


    if store_specific_accounts:
        Account(name='Bank OD', category=secured_loans, company=company).save()
        Account(name='Bank Loans', category=secured_loans, company=company).save()
        lotto_and_scratch_off = Category(name='Lotto and Scratch Off', parent=current_liabilities, company=company)
        lotto_and_scratch_off.save()
        lotto = Category(name='Lotto', parent=lotto_and_scratch_off, company=company)
        lotto.save()
        scratch_off = Category(name='Scratch Off', parent=lotto_and_scratch_off, company=company)
        scratch_off.save()
        Account(name='Scratch Off Sales', category=scratch_off, company=company).save()
        Account(name='Lotto Sales', category=lotto, company=company).save()
        Account(name='Scratch Off Purchase', category=scratch_off, company=company).save()
        Account(name='Lotto Purchase', category=lotto, company=company).save()
        Account(name='Scratch Off Payout', category=scratch_off, company=company).save()
        Account(name='Lotto Payout', category=lotto, company=company).save()
        transfer_remittance = Category(name='Transfer and Remittance', parent=current_liabilities, company=company)
        transfer_remittance.save()
        Account(name='MoneyGram', category=transfer_remittance, company=company).save()
        Account(name='Money Order', category=transfer_remittance, company=company).save()
        Account(name='Bill Payments', category=transfer_remittance, company=company).save()

        Category(name='Provisions', parent=current_liabilities, company=company).save()
        Category(name='Unsecured Loans', parent=current_liabilities, company=company).save()
        Category(name='Deposits Taken', parent=current_liabilities, company=company).save()
        Category(name='Loans & Advances Taken', parent=current_liabilities, company=company).save()
    duties_and_taxes = Category(name='Duties & Taxes', parent=current_liabilities, company=company)
    duties_and_taxes.save()
    if store_specific_accounts:
        sales_tax_account = Account(name='Sales Tax', category=duties_and_taxes, company=company)
        sales_tax_account.save()
        Account(name='Income Tax', category=duties_and_taxes, company=company).save()

    if store_specific_accounts:
        telephone_tax_account = Account(name='Telephone Tax', category=duties_and_taxes, company=company)
        telephone_tax_account.save()

    Category(name='Employee', parent=current_liabilities, company=company).save()
    employee_deductions = Category(name='Employee Deductions', parent=current_liabilities, company=company)
    employee_deductions.save()
    if store_specific_accounts:
        Account(name='Advances', category=employee_deductions, company=company).save()
        Account(name='Loans', category=employee_deductions, company=company).save()
        Account(name='Payroll Tax', category=employee_deductions, company=company).save()
        Account(name='Employees\' Contribution to Retirement Fund', category=employee_deductions, company=company).save()
        Account(name='Compulsory Deductions', category=employee_deductions, company=company).save()
    other_payables = Category(name='Other Payables', parent=current_liabilities, company=company)
    other_payables.save()
    if store_specific_accounts:
        Account(name='Utility Bills Account', category=other_payables, company=company).save()

    assets = Category(name='Assets', company=company)
    assets.save()
    non_current_assets = Category(name='Non Current Assets', parent=assets, company=company)
    non_current_assets.save()
    Category(name='Fixed Assets', parent=non_current_assets, company=company).save()
    Category(name='Investments', parent=non_current_assets, company=company).save()

    current_assets = Category(name='Current Assets', parent=assets, company=company)
    current_assets.save()
    Category(name='Deferred Assets', parent=current_assets, company=company).save()
    stock = Category(name='Stock', parent=current_assets, company=company)
    stock.save()
    Account(name='Opening Stock', category=stock, company=company).save()
    Account(name='Closing Stock', category=stock, company=company).save()
    Category(name='Loans and Advances Given', parent=current_assets, company=company).save()
    Category(name='Deposits Made', parent=current_assets, company=company).save()
    account_receivables = Category(name='Account Receivables', parent=current_assets, company=company)
    account_receivables.save()
    Category(name='Customers', parent=account_receivables, company=company).save()
    Category(name='Other Receivables', parent=account_receivables, company=company).save()
    Category(name='Other Current Assets', parent=current_assets, company=company)
    if store_specific_accounts:
        cash_equivalent_account = Category(name='Cash Equivalent Account', parent=current_assets, company=company)
        cash_equivalent_account.save()


    if store_specific_accounts:
        Account(name='Cheque Account', category=cash_equivalent_account, company=company).save()
        Account(name='Food Stamps Account', category=cash_equivalent_account, company=company).save()
        Account(name='Coupons Account', category=cash_equivalent_account, company=company).save()
        Account(name='Merchandise', category=current_assets, company=company).save()

    bank_account = Category(name='Bank Account', parent=current_assets, company=company)
    bank_account.save()
    Account(name='Bank Account', category=bank_account, company=company).save()
    if store_specific_accounts:
        Account(name='Card Account', category=bank_account, company=company).save()
        Account(name='ATM Account', category=bank_account, company=company).save()
    cash_account = Category(name='Cash Account', parent=current_assets, company=company)
    cash_account.save()
    Account(name='Cash Account', category=cash_account, company=company).save()

    income = Category(name='Income', company=company)
    income.save()
    direct_income = Category(name='Revenue', parent=income, company=company)
    direct_income.save()
    sales = Category(name='Sales', parent=direct_income, company=company)
    sales.save()

    if gas_station_specific:
        fuel_sales = Account(name='Fuel Sales', category=sales, company=company)
        fuel_sales.save()
    if store_specific_accounts:
        cigarette_tobacco_sales = Account(name='Cigarette/Tobacco Sales', category=sales, company=company)
        cigarette_tobacco_sales.save()
        soda_sales = Account(name='Soda Sales', category=sales, company=company)
        soda_sales.save()
        water_sales = Account(name='Water Sales', category=sales, company=company)
        water_sales.save()
        newspaper_sales = Account(name='Newspaper Sales', category=sales, company=company)
        newspaper_sales.save()
        non_tax_sales = Account(name='Non Tax Sales', category=sales, company=company)
        non_tax_sales.save()
        telephone_pp_card = Account(name='Telephone PP Card Sales', category=sales,
                company=company)
        telephone_pp_card.save()
        sales = Account(name='Sales', category=sales, company=company)
        sales.save()
    indirect_income = Category(name='Indirect Income', parent=income, company=company)
    indirect_income.save()
    if store_specific_accounts:
        Account(name='Discount Income', category=indirect_income, company=company).save()
        Account(name='Commission In', category=indirect_income, company=company).save()

    expenses = Category(name='Expenses', company=company)
    expenses.save()
    purchase = Category(name='Purchase', parent=expenses, company=company)
    purchase.save()

    if gas_station_specific:
        Account(name='Fuel Purchase', category=purchase, company=company).save()
    if store_specific_accounts:
        Account(name='Cigarette/Tobacco Purchase', category=purchase, company=company).save()
        Account(name='Soda Purchase', category=purchase, company=company).save()
        Account(name='Water Purchase', category=purchase, company=company).save()
        Account(name='Newspaper Purchase', category=purchase, company=company).save()
        Account(name='Non Tax Purchase', category=purchase, company=company).save()
        Account(name='Telephone PP Card Purchase', category=purchase, company=company).save()
        Account(name='Moneygram Purchase', category=purchase, company=company).save()
        Account(name='Purchase', category=purchase, company=company).save()

    direct_expenses = Category(name='Direct Expenses', parent=expenses, company=company)
    direct_expenses.save()

    indirect_expenses = Category(name='Indirect Expenses', parent=expenses, company=company)
    indirect_expenses.save()
    if store_specific_accounts:
        Account(name='Payroll Expenses', category=indirect_expenses, company=company).save()
        Account(name='Rent Expenses', category=indirect_expenses, company=company).save()
    if store_specific_accounts:
        Account(name='Commission Out', category=indirect_expenses, company=company).save()
        Account(name='Bank Charges Expenses', category=indirect_expenses, company=company).save()
        Account(name='Bank Interest Expenses', category=indirect_expenses, company=company).save()
        Account(name='Electricity Expenses', category=indirect_expenses, company=company).save()
        Account(name='City/Municipal Expenses', category=indirect_expenses, company=company).save()
        Account(name='Travelling and Conveyance Expenses', category=indirect_expenses, company=company).save()
        Account(name='Lunch and Refreshment Expenses', category=indirect_expenses, company=company).save()
        Account(name='Cleaning Expenses', category=indirect_expenses, company=company).save()
        Account(name='Discount Expenses', category=indirect_expenses, company=company).save()
        Account(name='Repairs and Maintenance Expenses', category=indirect_expenses, company=company).save()

    pay_head = Category(name='Pay Head', parent=indirect_expenses, company=company)
    pay_head.save()
    if store_specific_accounts:
        Account(name='Salary', category=pay_head, company=company).save()
        Account(name='Allowances', category=pay_head, company=company).save()
        Account(name='Benefits', category=pay_head, company=company).save()
        Account(name='Employees\' Insurance', category=pay_head, company=company).save()
        Account(name='Travelling Allowance', category=pay_head, company=company).save()
        Account(name='Daily Allowance', category=pay_head, company=company).save()

    from inventory.models import Category as InventoryCategory
    if gas_station_specific:
        InventoryCategory(name='Fuel and Gas', company=company).save()

    from core.models import CompanySetting, VoucherSetting

    company_setting = CompanySetting(company=company)
    company_setting.company_type = other_params.get('type_of_business')[0]
    company_setting.financial_year_starts_on = other_params.get('financial_year_start_date')[0]
    company_setting.financial_year_ends_on = other_params.get('books_closing_date')[0]
    company_setting.current_financial_year_started_on = datetime.datetime.strptime(
        other_params.get('books_start_date')[0], '%m/%d/%Y')
    if store_specific_accounts:
        company_setting.inventory_tracking = True
        company_setting.lotto_tracking = True
    elif gas_station_specific:
        company_setting.inventory_tracking = True
    else:
        company_setting.inventory_tracking = False
        company_setting.lotto_tracking = False
    company_setting.save()
    voucher_setting = VoucherSetting(company=company)
    voucher_setting.save()

    from ledger.models import TaxScheme
    no_tax = TaxScheme(name='No Tax', percent=0, company=company)
    if store_specific_accounts:
        secondary_tax = TaxScheme(name='Telephone PP Card Tax @ 2.00%', percent=2.0, collection_ledger=telephone_tax_account, company=company)
        secondary_tax.save()
        primary_tax = TaxScheme(name='Sales Tax @ 8.25%', percent=8.25, collection_ledger=sales_tax_account, company=company)
        primary_tax.save()
    no_tax.save()

    if store_specific_accounts:
        AccountTaxDetail(account=sales, pri_tax_scheme=primary_tax, company=company).save()
        AccountTaxDetail(account=cigarette_tobacco_sales, pri_tax_scheme=primary_tax, company=company).save()
        AccountTaxDetail(account=soda_sales, pri_tax_scheme=primary_tax, company=company).save()
        AccountTaxDetail(account=telephone_pp_card, pri_tax_scheme=primary_tax, sec_tax_scheme_1=secondary_tax, company=company).save()
        AccountTaxDetail(account=non_tax_sales, company=company, pri_tax_scheme=no_tax).save()
        AccountTaxDetail(account=newspaper_sales, company=company, pri_tax_scheme=no_tax).save()
        AccountTaxDetail(account=water_sales, company=company, pri_tax_scheme=no_tax).save()
    if gas_station_specific:
        AccountTaxDetail(account=fuel_sales, company=company, pri_tax_scheme=no_tax).save()

    for account in Account.objects.filter(company=company):
        account.opening_as_on_date = datetime.datetime.strptime(other_params.get('books_start_date')[0], '%m/%d/%Y')
        account.save()


class Role(models.Model):
    user = models.ForeignKey(User, related_name='roles')
    group = models.ForeignKey(Group, related_name='roles')
    company = models.ForeignKey(Company, related_name='roles')

    def __str__(self):
        return self.group.name

    class Meta:
        unique_together = ('user', 'group', 'company')


from registration.models import RegistrationProfile


def handle_new_user(sender, user, request, **kwargs):
    company = Company.objects.get(name='Test Company Inc')

    user.is_active = False
    user.full_name = request.POST.get('full_name')
    user.save()
    try:
        role = Role(user=user, group=Group.objects.get(name='Owner'), company=company)
        role.save()
    except Group.DoesNotExist:
        Group(name='Owner').save()
        role = Role(user=user, group=Group.objects.get(name='Owner'), company=company)
        role.save()


from registration.signals import user_registered

user_registered.connect(handle_new_user)


def create_company(request):
    pass


def group_required(*groups):
    def _dec(view_function):

        def _view(request, *args, **kwargs):
            allowed = False
            for role in request.roles:
                if role.group.name in groups:
                    allowed = True
                if allowed:
                    return view_function(request, *args, **kwargs)
                else:
                    if request.user.is_authenticated():
                        return HttpResponseForbidden("You don't have permission to view this page!")
                    else:
                        return redirect(settings.LOGIN_URL)

        return _view

    return _dec


def view_license_required():
    def _dec(view_function):

        def _view(request, *args, **kwargs):
            allowed = False
            licence = request.user.currently_activated_company.licence
            if licence:
                if licence.view_valid_from <= datetime.date.today() <= licence.view_valid_to:
                    allowed = True
                if allowed:
                    return view_function(request, *args, **kwargs)
                else:
                    if request.user.is_authenticated():
                        return HttpResponseForbidden("You don't have permission to view this page!")
                    else:
                        return redirect(settings.LOGIN_URL)
            else:
                return redirect(settings.LOGIN_URL)

        return _view

    return _dec


def create_license_required():
    def _dec(view_function):

        def _view(request, *args, **kwargs):
            allowed = False
            for licence in request.user.currently_activated_company.licence:
                if licence.create_valid_from <= datetime.date.today() <= licence.create_valid_to:
                    allowed = True
                if allowed:
                    return view_function(request, *args, **kwargs)
                else:
                    if request.user.is_authenticated():
                        return HttpResponseForbidden("You don't have permission to view this page!")
                    else:
                        return redirect(settings.LOGIN_URL)
            else:
                return redirect(settings.LOGIN_URL)

        return _view

    return _dec


# class UserSalesAttachment(models.Model):
#     attachment = models.FileField(upload_to='user_day_sales_attachments/%Y/%m/%d')
#     description = models.CharField(max_length=254)
#     company = models.ForeignKey(Company, related_name='user_sales_attachments')
#
#
# class UserPurchaseAttachment(models.Model):
#     attachment = models.FileField(upload_to='user_day_purchase_attachments/%Y/%m/%d')
#     description = models.CharField(max_length=254)
#     company = models.ForeignKey(Company, related_name='user_purchase_attachments')
#
#
# class UserBankAttachment(models.Model):
#     attachment = models.FileField(upload_to='user_day_bank_attachments/%Y/%m/%d')
#     description = models.CharField(max_length=254)
#     company = models.ForeignKey(Company, related_name='user_bank_attachments')
#
#
# class UserOtherAttachment(models.Model):
#     attachment = models.FileField(upload_to='user_day_other_attachments/%Y/%m/%d')
#     description = models.CharField(max_length=254)
#     company = models.ForeignKey(Company, related_name='user_other_attachments')


class UserSalesAttachment(models.Model):
    attachment = models.FileField(upload_to='user_day_sales_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    company = models.ForeignKey(Company, related_name='user_sales_attachments')
    uploaded_date = models.DateTimeField(null=True)
    uploaded_time = models.TimeField(null=True)
    processed_date = models.DateTimeField(null=True)
    is_processed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)


class UserPurchaseAttachment(models.Model):
    attachment = models.FileField(upload_to='user_day_purchase_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    company = models.ForeignKey(Company, related_name='user_purchase_attachments')
    uploaded_date = models.DateTimeField(null=True)
    uploaded_time = models.TimeField(null=True)
    processed_date = models.DateTimeField(null=True)
    is_processed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)


class UserBankAttachment(models.Model):
    attachment = models.FileField(upload_to='user_day_bank_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    company = models.ForeignKey(Company, related_name='user_bank_attachments')
    uploaded_date = models.DateTimeField(null=True)
    uploaded_time = models.TimeField(null=True)
    processed_date = models.DateTimeField(null=True)
    is_processed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)


class UserOtherAttachment(models.Model):
    attachment = models.FileField(upload_to='user_day_other_attachments/%Y/%m/%d')
    description = models.CharField(max_length=254)
    company = models.ForeignKey(Company, related_name='user_other_attachments')
    uploaded_date = models.DateTimeField(null=True)
    uploaded_time = models.TimeField(null=True)
    processed_date = models.DateTimeField(null=True)
    is_processed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)


class TrackUserInfo(models.Model):
    ipaddress = models.CharField(max_length=20)
    count = models.IntegerField(default=1)
    country = models.CharField(max_length=10, null=True)
    continent = models.CharField(max_length=10, null=True)
    timezone = models.CharField(max_length=100, null=True)
    latitude = models.IntegerField(null=True)
    longitude = models.IntegerField(null=True)
    # country = models.CharField(max_length=50)
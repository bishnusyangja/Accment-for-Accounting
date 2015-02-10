import datetime

from django.db import models

from users.models import Company


class Currency(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    latest_usd_rate = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = u'Currencies'
        db_table = 'currency'

    def __unicode__(self):
        return self.code + ' - ' + self.name


class CompanySetting(models.Model):
    company = models.OneToOneField(Company, related_name='settings')
    #default_currency = models.ForeignKey(Currency, null=True)
    decimal_places = models.IntegerField(default=2)
    number_comma_system = models.CharField(
        choices=[('120,000', '120,000'), ('1,20,000', '1,20,000'), ('no', 'No Commas')], max_length=8,
        default='120,000')
    region_setting = models.CharField(
        choices=[('North America', 'North America'), ('South America', 'South America'), ('Europe', 'Europe'),
                 ('Africa', 'Africa'), ('Asia/Pacific', 'Asia/Pacific')], max_length=15, default='North America')
    account_coding = models.CharField(choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')], max_length=9,
                                      default='Automatic')
    lotto_tracking = models.BooleanField()
    inventory_tracking = models.BooleanField()
    company_type = models.CharField(max_length=50, default='Gas Station and Store')
    financial_year_starts_on = models.CharField(max_length=5, null=True)
    financial_year_ends_on = models.CharField(max_length=5, null=True)
    current_financial_year_started_on = models.DateField(default=datetime.date.today())
    registered_date = models.DateField(default=datetime.date.today())

    def __unicode__(self):
        return self.company.name


class VoucherSetting(models.Model):
    company = models.OneToOneField(Company, related_name='voucher_settings')
    voucher_number_start_date = models.DateField(default=datetime.date.today())
    voucher_number_restart_years = models.IntegerField(default=1)
    voucher_number_restart_months = models.IntegerField(default=0)
    voucher_number_restart_days = models.IntegerField(default=0)

    invoice_prefix = models.CharField(max_length=5, default='INV', blank=True, null=True)
    invoice_suffix = models.CharField(max_length=5, default=str(datetime.date.today().year), blank=True, null=True)
    purchase_voucher_prefix = models.CharField(max_length=5, default='PV', blank=True, null=True)
    purchase_voucher_suffix = models.CharField(max_length=5, default=str(datetime.date.today().year), blank=True, null=True)
    fixed_assets_prefix = models.CharField(max_length=5, default='FA', blank=True, null=True)
    fixed_assets_suffix = models.CharField(max_length=5, default=str(datetime.date.today().year), blank=True, null=True)
    journal_voucher_prefix = models.CharField(max_length=5, default='JV', blank=True, null=True)
    journal_voucher_suffix = models.CharField(max_length=5, default=str(datetime.date.today().year), blank=True, null=True)
    cash_receipt_prefix = models.CharField(max_length=5, default='CR', blank=True, null=True)
    cash_receipt_suffix = models.CharField(max_length=5, default=str(datetime.date.today().year), blank=True, null=True)
    cash_payment_prefix = models.CharField(max_length=5, default='CP', blank=True, null=True)
    cash_payment_suffix = models.CharField(max_length=5, default=str(datetime.date.today().year), blank=True, null=True)
    bank_deposit_prefix = models.CharField(max_length=5, default='BD', blank=True, null=True)
    bank_deposit_suffix = models.CharField(max_length=5, default=str(datetime.date.today().year), blank=True, null=True)
    bank_payment_prefix = models.CharField(max_length=5, default='BP', blank=True, null=True)
    bank_payment_suffix = models.CharField(max_length=5, default=str(datetime.date.today().year), blank=True, null=True)
    physicalstock_prefix = models.CharField(max_length=5, default='PS', blank=True, null=True)
    physicalstock_suffix = models.CharField(max_length=5, default=str(datetime.date.today().year), blank=True, null=True)


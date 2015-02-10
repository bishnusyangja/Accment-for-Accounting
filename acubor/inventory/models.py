from datetime import datetime, date

from django.db import models
from django.db.models import Sum
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from users.models import Company
from lib import get_next_voucher_no, zero_for_none


class Category(MPTTModel):
    name = models.CharField(max_length=50, verbose_name="Name *")
    description = models.CharField(max_length=254, null=True, blank=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children')
    company = models.ForeignKey(Company, related_name='inventory_categories')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/category/' + str(self.id)

    def get_company(self):
        return self.company


class InventoryAccount(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)

    def get_current_stock(self, till_date):
        stock_entries = InventoryLedger.objects.filter(account=self, company=self.company, date__lt=till_date)
        current_stock = 0
        for each in stock_entries:
            current_stock = current_stock + zero_for_none(each.in_quantity)
            current_stock = current_stock - zero_for_none(each.out_quantity)
        return current_stock

    def get_absolute_url(self):
        return '/inventory_account/' + str(self.id)

    def get_unit(self):
        try:
            item = self.item
        except:
            return None
        try:
            short_name = self.item.unit.short_name
        except:
            return None
        return short_name

    def get_category(self):
        try:
            item = self.item
        except:
            return None
        try:
            category = self.item.category
        except:
            return None
        return category

    def __unicode__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name *")
    short_name = models.CharField(max_length=10, verbose_name="Short Name *")
    company = models.ForeignKey(Company, related_name='inventory_units')

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=254, verbose_name="Name *")
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, related_name='inventory_items')
    category = models.ForeignKey(Category, related_name='items', null=True, blank=True)
    account = models.OneToOneField(InventoryAccount, related_name='item')
    opening_stock_quantity = models.FloatField(default=0)
    unit = models.ForeignKey(Unit, related_name='items', null=True, verbose_name="Unit *")

    def save(self, *args, **kwargs):
        if self.pk is None:
            account = InventoryAccount(name=self.name, company=self.company)
            account.save()
            self.account = account
        super(Item, self).save(*args, **kwargs)

    def add_category(self, category):
        category_instance, created = Category.objects.get_or_create(name=category)
        self.categories.add(category_instance)

    def get_unit(self):
        try:
            short_name = self.unit.short_name
        except:
            return None
        return short_name

    def get_current_stock(self, till_date):
        return zero_for_none(self.account.get_current_stock(till_date)) + zero_for_none(self.opening_stock_quantity)

    def __unicode__(self):
        return self.name


class InventoryLedger(models.Model):
    date = models.DateField(null=True)
    company = models.ForeignKey(Company, null=True, related_name='inventory_transactions')
    account = models.ForeignKey(InventoryAccount, null=True, related_name='inventory_transactions')
    in_quantity = models.FloatField(default=0)
    out_quantity = models.FloatField(default=0)
    in_rate = models.FloatField(default=0)
    out_rate = models.FloatField(default=0)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    source = generic.GenericForeignKey('content_type', 'object_id')

    def in_amount(self):
        in_quantity = 0
        if self.in_quantity:
            in_quantity = self.in_quantity
        rate = self.in_rate
        return in_quantity * rate

    def out_amount(self):
        out_quantity = 0
        if self.out_quantity:
            out_quantity = self.out_quantity
        rate = self.out_rate
        return out_quantity * rate

    def get_balance_rate(self):
        return self.in_rate

    def get_balance_quantity(self):
        agg = InventoryLedger.objects.filter(company=self.company, account=self.account, date__lte=date.today(),
                                             id__lte=self.id).aggregate(in_total=Sum('in_quantity'),
                                                                        out_total=Sum('out_quantity'))
        if agg['in_total'] > agg['out_total']:
            return agg['in_total'] - agg['out_total']
        elif agg['in_total'] < agg['out_total']:
            return agg['out_total'] - agg['in_total']
        else:
            return 0

    def get_balance_amount(self):
        return self.get_balance_quantity() * self.get_balance_rate()


class PhysicalStockVoucher(models.Model):
    date = models.DateField(null=True, blank=True)
    voucher_no = models.IntegerField(null=True, verbose_name='Voucher No.')
    company = models.ForeignKey(Company, related_name='physical_stock_vouchers')
    statuses = [('Cancelled', 'Cancelled'), ('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')
    total_amount = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'physical_stock_voucher'

    def get_total_amount(self):
        return self.total_amount

    def get_voucher_no(self):
        return self.voucher_no

    def get_voucher_description(self):
        return self.description

    def get_absolute_url(self):
        return '/inventory/physicalstock/' + self.physical_stock_voucher.voucher_no + '/'

    def __init__(self, *args, **kwargs):
        super(PhysicalStockVoucher, self).__init__(*args, **kwargs)
        if not self.pk and not self.voucher_no:
            self.voucher_no = get_next_voucher_no(PhysicalStockVoucher, self.company)

    def backend_approve(self):
        if self.status == 'Unapproved':
            for row in self.particulars.all():
                if row.item:
                    net_balance_quantity = row.item.get_current_stock(self.date)
                    net_required_quantity = zero_for_none(row.quantity) - net_balance_quantity
                    if net_required_quantity < 0:
                        out_quantity = -1 * net_required_quantity
                        InventoryLedger(date=self.date, company=self.company, account=row.item.account,
                                        in_quantity=0, out_quantity=out_quantity, in_rate=0, out_rate=row.rate,
                                        content_type=ContentType.objects.get(model='physicalstockvoucher'),
                                        object_id=self.id).save()
                    elif net_required_quantity > 0:
                        in_quantity = net_required_quantity
                        InventoryLedger(date=self.date, company=self.company, account=row.item.account,
                                        in_quantity=in_quantity, out_quantity=0, in_rate=row.rate, out_rate=0,
                                        content_type=ContentType.objects.get(model='physicalstockvoucher'),
                                        object_id=self.id).save()
                    else:
                        continue
            self.status = 'Approved'
            self.save()
        return self.status

    def backend_unapprove(self):
        ctype = ContentType.objects.get(model='physicalstockvoucher')
        InventoryLedger.objects.filter(content_type=ctype, object_id=self.id).delete()
        self.status = 'Unapproved'
        self.save()
        return self.status


class PhysicalStockRow(models.Model):
    sn = models.IntegerField()
    item = models.ForeignKey(Item)
    description = models.TextField()
    quantity = models.FloatField(default=0)
    rate = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    physical_stock_voucher = models.ForeignKey(PhysicalStockVoucher, related_name='particulars')
    unit = models.ForeignKey(Unit, blank=True, null=True)

    def get_absolute_url(self):
        return '/inventory/physicalstock/' + self.physical_stock_voucher.voucher_no + '/'

    def get_voucher_no(self):
        return self.physical_stock_voucher.voucher_no

    def get_voucher_description(self):
        return self.physical_stock_voucher.description

    class Meta:
        db_table = 'physical_stock_row'

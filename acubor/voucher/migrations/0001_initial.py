# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invoice'
        db.create_table('invoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Party'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Currency'], null=True, blank=True)),
            ('tax', self.gf('django.db.models.fields.CharField')(default='inclusive', max_length=10, null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
            ('pending_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('total_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'voucher', ['Invoice'])

        # Adding model 'InvoiceParticular'
        db.create_table('invoice_particular', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('quantity', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('discount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'], null=True, blank=True)),
            ('tax_scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.TaxScheme'], null=True, blank=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='particulars', to=orm['voucher.Invoice'])),
        ))
        db.send_create_signal(u'voucher', ['InvoiceParticular'])

        # Adding model 'PurchaseVoucher'
        db.create_table(u'voucher_purchasevoucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Party'], null=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Currency'])),
            ('tax', self.gf('django.db.models.fields.CharField')(default='inclusive', max_length=10)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('pending_amount', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('total_amount', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'voucher', ['PurchaseVoucher'])

        # Adding model 'PurchaseParticular'
        db.create_table('purchase_particular', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Item'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('quantity', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('unit_price', self.gf('django.db.models.fields.FloatField')()),
            ('discount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'], null=True, blank=True)),
            ('tax_scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.TaxScheme'], null=True, blank=True)),
            ('purchase_voucher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='particulars', to=orm['voucher.PurchaseVoucher'])),
        ))
        db.send_create_signal(u'voucher', ['PurchaseParticular'])

        # Adding model 'JournalVoucher'
        db.create_table(u'voucher_journalvoucher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('narration', self.gf('django.db.models.fields.TextField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'voucher', ['JournalVoucher'])

        # Adding model 'JournalVoucherRow'
        db.create_table(u'voucher_journalvoucherrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Dr', max_length=2)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='account_rows', to=orm['ledger.Account'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dr_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cr_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('journal_voucher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['voucher.JournalVoucher'])),
        ))
        db.send_create_signal(u'voucher', ['JournalVoucherRow'])

        # Adding model 'CashReceipt'
        db.create_table(u'voucher_cashreceipt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('cash_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_receipt', null=True, to=orm['ledger.Account'])),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'voucher', ['CashReceipt'])

        # Adding model 'CashReceiptRow'
        db.create_table(u'voucher_cashreceiptrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('from_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'], null=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('reference_no', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('cash_receipt', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['voucher.CashReceipt'])),
        ))
        db.send_create_signal(u'voucher', ['CashReceiptRow'])

        # Adding model 'CashPayment'
        db.create_table(u'voucher_cashpayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('cash_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_payment', null=True, to=orm['ledger.Account'])),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'voucher', ['CashPayment'])

        # Adding model 'CashPaymentRow'
        db.create_table(u'voucher_cashpaymentrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('to_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'], null=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('reference_no', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('cash_payment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['voucher.CashPayment'])),
        ))
        db.send_create_signal(u'voucher', ['CashPaymentRow'])

        # Adding model 'FixedAsset'
        db.create_table(u'voucher_fixedasset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'voucher', ['FixedAsset'])

        # Adding model 'FixedAssetRow'
        db.create_table(u'voucher_fixedassetrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset_ledger', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('fixed_asset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['voucher.FixedAsset'])),
        ))
        db.send_create_signal(u'voucher', ['FixedAssetRow'])

        # Adding model 'AdditionalDetail'
        db.create_table(u'voucher_additionaldetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assets_code', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('assets_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('vendor_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('vendor_address', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('useful_life', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('warranty_period', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('maintenance', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('fixed_asset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='additional_details', to=orm['voucher.FixedAsset'])),
        ))
        db.send_create_signal(u'voucher', ['AdditionalDetail'])


    def backwards(self, orm):
        # Deleting model 'Invoice'
        db.delete_table('invoice')

        # Deleting model 'InvoiceParticular'
        db.delete_table('invoice_particular')

        # Deleting model 'PurchaseVoucher'
        db.delete_table(u'voucher_purchasevoucher')

        # Deleting model 'PurchaseParticular'
        db.delete_table('purchase_particular')

        # Deleting model 'JournalVoucher'
        db.delete_table(u'voucher_journalvoucher')

        # Deleting model 'JournalVoucherRow'
        db.delete_table(u'voucher_journalvoucherrow')

        # Deleting model 'CashReceipt'
        db.delete_table(u'voucher_cashreceipt')

        # Deleting model 'CashReceiptRow'
        db.delete_table(u'voucher_cashreceiptrow')

        # Deleting model 'CashPayment'
        db.delete_table(u'voucher_cashpayment')

        # Deleting model 'CashPaymentRow'
        db.delete_table(u'voucher_cashpaymentrow')

        # Deleting model 'FixedAsset'
        db.delete_table(u'voucher_fixedasset')

        # Deleting model 'FixedAssetRow'
        db.delete_table(u'voucher_fixedassetrow')

        # Deleting model 'AdditionalDetail'
        db.delete_table(u'voucher_additionaldetail')


    models = {
        u'core.currency': {
            'Meta': {'object_name': 'Currency', 'db_table': "'currency'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_usd_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'inventory.category': {
            'Meta': {'unique_together': "(('company', 'name'),)", 'object_name': 'Category'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_categories'", 'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['inventory.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'inventory.inventoryaccount': {
            'Meta': {'object_name': 'InventoryAccount'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_cr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'current_dr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'opening_balance': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'item'", 'unique': 'True', 'to': u"orm['inventory.InventoryAccount']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Category']", 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_stock': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'opening_stock': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'purchase_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_items'", 'to': u"orm['ledger.Account']"}),
            'purchase_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'purchase_tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_items'", 'to': u"orm['ledger.TaxScheme']"}),
            'sales_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sales_items'", 'to': u"orm['ledger.Account']"}),
            'sales_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sales_tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sales_items'", 'to': u"orm['ledger.TaxScheme']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Unit']", 'null': 'True', 'blank': 'True'})
        },
        u'inventory.unit': {
            'Meta': {'object_name': 'Unit'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'ledger.account': {
            'Meta': {'unique_together': "(('company', 'name'),)", 'object_name': 'Account'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'blank': 'True', 'to': u"orm['ledger.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_cr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'current_dr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_scheme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'account'", 'null': 'True', 'to': u"orm['ledger.InterestScheme']"}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'opening_as_on_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
            'opening_cr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'opening_dr': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'ledger.category': {
            'Meta': {'unique_together': "(('company', 'name'),)", 'object_name': 'Category'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ledger.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'ledger.interestscheme': {
            'Meta': {'object_name': 'InterestScheme'},
            'collection_ledger': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'int_scheme'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_period': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rate_in_pct': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'ledger.party': {
            'Meta': {'object_name': 'Party', 'db_table': "'party'"},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'customer_account': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'customer_detail'", 'unique': 'True', 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'supplier_account': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'supplier_detail'", 'unique': 'True', 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Customer'", 'max_length': '17'})
        },
        u'ledger.taxscheme': {
            'Meta': {'object_name': 'TaxScheme'},
            'collection_ledger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tax_scheme'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'percent': ('django.db.models.fields.FloatField', [], {})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        },
        u'voucher.additionaldetail': {
            'Meta': {'object_name': 'AdditionalDetail'},
            'amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'assets_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'assets_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fixed_asset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'additional_details'", 'to': u"orm['voucher.FixedAsset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintenance': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'useful_life': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'vendor_address': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'vendor_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'warranty_period': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'voucher.cashpayment': {
            'Meta': {'object_name': 'CashPayment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cash_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_payment'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'voucher.cashpaymentrow': {
            'Meta': {'object_name': 'CashPaymentRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'cash_payment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['voucher.CashPayment']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'to_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']", 'null': 'True'})
        },
        u'voucher.cashreceipt': {
            'Meta': {'object_name': 'CashReceipt'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cash_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_receipt'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'voucher.cashreceiptrow': {
            'Meta': {'object_name': 'CashReceiptRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'cash_receipt': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['voucher.CashReceipt']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'from_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'voucher.fixedasset': {
            'Meta': {'object_name': 'FixedAsset'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'from_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'voucher.fixedassetrow': {
            'Meta': {'object_name': 'FixedAssetRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'asset_ledger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fixed_asset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['voucher.FixedAsset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'voucher.invoice': {
            'Meta': {'object_name': 'Invoice', 'db_table': "'invoice'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Currency']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Party']", 'null': 'True', 'blank': 'True'}),
            'pending_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'tax': ('django.db.models.fields.CharField', [], {'default': "'inclusive'", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'total_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'voucher.invoiceparticular': {
            'Meta': {'object_name': 'InvoiceParticular', 'db_table': "'invoice_particular'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'particulars'", 'to': u"orm['voucher.Invoice']"}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.TaxScheme']", 'null': 'True', 'blank': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        u'voucher.journalvoucher': {
            'Meta': {'object_name': 'JournalVoucher'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'voucher.journalvoucherrow': {
            'Meta': {'object_name': 'JournalVoucherRow'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'account_rows'", 'to': u"orm['ledger.Account']"}),
            'cr_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dr_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal_voucher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['voucher.JournalVoucher']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Dr'", 'max_length': '2'})
        },
        u'voucher.purchaseparticular': {
            'Meta': {'object_name': 'PurchaseParticular', 'db_table': "'purchase_particular'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'purchase_voucher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'particulars'", 'to': u"orm['voucher.PurchaseVoucher']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.TaxScheme']", 'null': 'True', 'blank': 'True'}),
            'unit_price': ('django.db.models.fields.FloatField', [], {})
        },
        u'voucher.purchasevoucher': {
            'Meta': {'object_name': 'PurchaseVoucher'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Currency']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Party']", 'null': 'True'}),
            'pending_amount': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'tax': ('django.db.models.fields.CharField', [], {'default': "'inclusive'", 'max_length': '10'}),
            'total_amount': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['voucher']
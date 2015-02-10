# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'VoucherSetting.journal_voucher_heading'
        db.delete_column(u'core_vouchersetting', 'journal_voucher_heading')

        # Deleting field 'VoucherSetting.purchase_voucher_heading'
        db.delete_column(u'core_vouchersetting', 'purchase_voucher_heading')

        # Deleting field 'VoucherSetting.bank_cash_deposit_heading'
        db.delete_column(u'core_vouchersetting', 'bank_cash_deposit_heading')

        # Deleting field 'VoucherSetting.eft_in_suffix'
        db.delete_column(u'core_vouchersetting', 'eft_in_suffix')

        # Deleting field 'VoucherSetting.bank_cash_deposit_suffix'
        db.delete_column(u'core_vouchersetting', 'bank_cash_deposit_suffix')

        # Deleting field 'VoucherSetting.cheque_deposit_heading'
        db.delete_column(u'core_vouchersetting', 'cheque_deposit_heading')

        # Deleting field 'VoucherSetting.fixed_assets_heading'
        db.delete_column(u'core_vouchersetting', 'fixed_assets_heading')

        # Deleting field 'VoucherSetting.invoice_heading'
        db.delete_column(u'core_vouchersetting', 'invoice_heading')

        # Deleting field 'VoucherSetting.cheque_deposit_suffix'
        db.delete_column(u'core_vouchersetting', 'cheque_deposit_suffix')

        # Deleting field 'VoucherSetting.eft_out_heading'
        db.delete_column(u'core_vouchersetting', 'eft_out_heading')

        # Deleting field 'VoucherSetting.cash_receipt_heading'
        db.delete_column(u'core_vouchersetting', 'cash_receipt_heading')

        # Deleting field 'VoucherSetting.bank_cash_deposit_prefix'
        db.delete_column(u'core_vouchersetting', 'bank_cash_deposit_prefix')

        # Deleting field 'VoucherSetting.cash_payment_heading'
        db.delete_column(u'core_vouchersetting', 'cash_payment_heading')

        # Deleting field 'VoucherSetting.physicalstock_heading'
        db.delete_column(u'core_vouchersetting', 'physicalstock_heading')

        # Deleting field 'VoucherSetting.eft_in_prefix'
        db.delete_column(u'core_vouchersetting', 'eft_in_prefix')

        # Deleting field 'VoucherSetting.cheque_deposit_prefix'
        db.delete_column(u'core_vouchersetting', 'cheque_deposit_prefix')

        # Deleting field 'VoucherSetting.eft_in_heading'
        db.delete_column(u'core_vouchersetting', 'eft_in_heading')

        # Deleting field 'VoucherSetting.cheque_payment_heading'
        db.delete_column(u'core_vouchersetting', 'cheque_payment_heading')

        # Adding field 'VoucherSetting.bank_deposit_prefix'
        db.add_column(u'core_vouchersetting', 'bank_deposit_prefix',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VoucherSetting.bank_deposit_suffix'
        db.add_column(u'core_vouchersetting', 'bank_deposit_suffix',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VoucherSetting.bank_payment_prefix'
        db.add_column(u'core_vouchersetting', 'bank_payment_prefix',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VoucherSetting.bank_payment_suffix'
        db.add_column(u'core_vouchersetting', 'bank_payment_suffix',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'VoucherSetting.journal_voucher_heading'
        db.add_column(u'core_vouchersetting', 'journal_voucher_heading',
                      self.gf('django.db.models.fields.CharField')(default='Journal Voucher', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.purchase_voucher_heading'
        db.add_column(u'core_vouchersetting', 'purchase_voucher_heading',
                      self.gf('django.db.models.fields.CharField')(default='Purchase Voucher', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.bank_cash_deposit_heading'
        db.add_column(u'core_vouchersetting', 'bank_cash_deposit_heading',
                      self.gf('django.db.models.fields.CharField')(default='Bank Cash Deposit', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.eft_in_suffix'
        db.add_column(u'core_vouchersetting', 'eft_in_suffix',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VoucherSetting.bank_cash_deposit_suffix'
        db.add_column(u'core_vouchersetting', 'bank_cash_deposit_suffix',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VoucherSetting.cheque_deposit_heading'
        db.add_column(u'core_vouchersetting', 'cheque_deposit_heading',
                      self.gf('django.db.models.fields.CharField')(default='Cheque Deposit', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.fixed_assets_heading'
        db.add_column(u'core_vouchersetting', 'fixed_assets_heading',
                      self.gf('django.db.models.fields.CharField')(default='Fixed Assets Voucher', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.invoice_heading'
        db.add_column(u'core_vouchersetting', 'invoice_heading',
                      self.gf('django.db.models.fields.CharField')(default='Invoice', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.cheque_deposit_suffix'
        db.add_column(u'core_vouchersetting', 'cheque_deposit_suffix',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VoucherSetting.eft_out_heading'
        db.add_column(u'core_vouchersetting', 'eft_out_heading',
                      self.gf('django.db.models.fields.CharField')(default='EFT Out', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.cash_receipt_heading'
        db.add_column(u'core_vouchersetting', 'cash_receipt_heading',
                      self.gf('django.db.models.fields.CharField')(default='Cash Receipt', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.bank_cash_deposit_prefix'
        db.add_column(u'core_vouchersetting', 'bank_cash_deposit_prefix',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VoucherSetting.cash_payment_heading'
        db.add_column(u'core_vouchersetting', 'cash_payment_heading',
                      self.gf('django.db.models.fields.CharField')(default='Cash Payment', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.physicalstock_heading'
        db.add_column(u'core_vouchersetting', 'physicalstock_heading',
                      self.gf('django.db.models.fields.CharField')(default='Physical Stock Voucher', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.eft_in_prefix'
        db.add_column(u'core_vouchersetting', 'eft_in_prefix',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VoucherSetting.cheque_deposit_prefix'
        db.add_column(u'core_vouchersetting', 'cheque_deposit_prefix',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'VoucherSetting.eft_in_heading'
        db.add_column(u'core_vouchersetting', 'eft_in_heading',
                      self.gf('django.db.models.fields.CharField')(default='EFT In', max_length=100),
                      keep_default=False)

        # Adding field 'VoucherSetting.cheque_payment_heading'
        db.add_column(u'core_vouchersetting', 'cheque_payment_heading',
                      self.gf('django.db.models.fields.CharField')(default='Cheque Payment', max_length=100),
                      keep_default=False)

        # Deleting field 'VoucherSetting.bank_deposit_prefix'
        db.delete_column(u'core_vouchersetting', 'bank_deposit_prefix')

        # Deleting field 'VoucherSetting.bank_deposit_suffix'
        db.delete_column(u'core_vouchersetting', 'bank_deposit_suffix')

        # Deleting field 'VoucherSetting.bank_payment_prefix'
        db.delete_column(u'core_vouchersetting', 'bank_payment_prefix')

        # Deleting field 'VoucherSetting.bank_payment_suffix'
        db.delete_column(u'core_vouchersetting', 'bank_payment_suffix')


    models = {
        u'core.companysetting': {
            'Meta': {'object_name': 'CompanySetting'},
            'account_coding': ('django.db.models.fields.CharField', [], {'default': "'Automatic'", 'max_length': '9'}),
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'settings'", 'unique': 'True', 'to': u"orm['users.Company']"}),
            'company_type': ('django.db.models.fields.CharField', [], {'default': "'Gas Station and Store'", 'max_length': '50'}),
            'current_financial_year_started_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 28, 0, 0)'}),
            'decimal_places': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'financial_year_ends_on': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'financial_year_starts_on': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory_tracking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lotto_tracking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_comma_system': ('django.db.models.fields.CharField', [], {'default': "'120,000'", 'max_length': '8'}),
            'region_setting': ('django.db.models.fields.CharField', [], {'default': "'North America'", 'max_length': '15'}),
            'registered_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 28, 0, 0)'})
        },
        u'core.currency': {
            'Meta': {'object_name': 'Currency', 'db_table': "'currency'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_usd_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.vouchersetting': {
            'Meta': {'object_name': 'VoucherSetting'},
            'bank_deposit_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'bank_deposit_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'bank_payment_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'bank_payment_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_payment_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_payment_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_receipt_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_receipt_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'voucher_settings'", 'unique': 'True', 'to': u"orm['users.Company']"}),
            'fixed_assets_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'fixed_assets_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'invoice_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'journal_voucher_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'journal_voucher_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'physicalstock_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'physicalstock_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'purchase_voucher_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'purchase_voucher_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'voucher_number_restart_days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'voucher_number_restart_months': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'voucher_number_restart_years': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'voucher_number_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 28, 0, 0)'})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            'address_line_1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_line_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'owner_full_name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']
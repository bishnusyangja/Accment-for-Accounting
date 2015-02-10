# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table('currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latest_usd_rate', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Currency'])

        # Adding model 'CompanySetting'
        db.create_table(u'core_companysetting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.OneToOneField')(related_name='settings', unique=True, to=orm['users.Company'])),
            ('decimal_places', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('number_comma_system', self.gf('django.db.models.fields.CharField')(default='120,000', max_length=8)),
            ('region_setting', self.gf('django.db.models.fields.CharField')(default='North America', max_length=15)),
            ('account_coding', self.gf('django.db.models.fields.CharField')(default='Automatic', max_length=9)),
        ))
        db.send_create_signal(u'core', ['CompanySetting'])

        # Adding model 'VoucherSetting'
        db.create_table(u'core_vouchersetting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.OneToOneField')(related_name='voucher_settings', unique=True, to=orm['users.Company'])),
            ('voucher_number_start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('voucher_number_restart_years', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('voucher_number_restart_months', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('voucher_number_restart_days', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('invoice_heading', self.gf('django.db.models.fields.CharField')(default='Invoice', max_length=100)),
            ('invoice_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('invoice_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('purchase_voucher_heading', self.gf('django.db.models.fields.CharField')(default='Purchase Voucher', max_length=100)),
            ('purchase_voucher_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('purchase_voucher_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('fixed_assets_heading', self.gf('django.db.models.fields.CharField')(default='Fixed Assets Voucher', max_length=100)),
            ('fixed_assets_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('fixed_assets_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('journal_voucher_heading', self.gf('django.db.models.fields.CharField')(default='Journal Voucher', max_length=100)),
            ('journal_voucher_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('journal_voucher_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('cash_receipt_heading', self.gf('django.db.models.fields.CharField')(default='Cash Receipt', max_length=100)),
            ('cash_receipt_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('cash_receipt_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('cash_payment_heading', self.gf('django.db.models.fields.CharField')(default='Cash Payment', max_length=100)),
            ('cash_payment_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('cash_payment_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('bank_cash_deposit_heading', self.gf('django.db.models.fields.CharField')(default='Bank Cash Deposit', max_length=100)),
            ('bank_cash_deposit_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('bank_cash_deposit_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('cheque_deposit_heading', self.gf('django.db.models.fields.CharField')(default='Cheque Deposit', max_length=100)),
            ('cheque_deposit_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('cheque_deposit_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('cheque_payment_heading', self.gf('django.db.models.fields.CharField')(default='Cheque Payment', max_length=100)),
            ('eft_in_heading', self.gf('django.db.models.fields.CharField')(default='EFT In', max_length=100)),
            ('eft_in_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('eft_in_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('eft_out_heading', self.gf('django.db.models.fields.CharField')(default='EFT Out', max_length=100)),
            ('physicalstock_heading', self.gf('django.db.models.fields.CharField')(default='Physical Stock Voucher', max_length=100)),
            ('physicalstock_prefix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
            ('physicalstock_suffix', self.gf('django.db.models.fields.CharField')(default='', max_length=5, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['VoucherSetting'])


    def backwards(self, orm):
        # Deleting model 'Currency'
        db.delete_table('currency')

        # Deleting model 'CompanySetting'
        db.delete_table(u'core_companysetting')

        # Deleting model 'VoucherSetting'
        db.delete_table(u'core_vouchersetting')


    models = {
        u'core.companysetting': {
            'Meta': {'object_name': 'CompanySetting'},
            'account_coding': ('django.db.models.fields.CharField', [], {'default': "'Automatic'", 'max_length': '9'}),
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'settings'", 'unique': 'True', 'to': u"orm['users.Company']"}),
            'decimal_places': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_comma_system': ('django.db.models.fields.CharField', [], {'default': "'120,000'", 'max_length': '8'}),
            'region_setting': ('django.db.models.fields.CharField', [], {'default': "'North America'", 'max_length': '15'})
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
            'bank_cash_deposit_heading': ('django.db.models.fields.CharField', [], {'default': "'Bank Cash Deposit'", 'max_length': '100'}),
            'bank_cash_deposit_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'bank_cash_deposit_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_payment_heading': ('django.db.models.fields.CharField', [], {'default': "'Cash Payment'", 'max_length': '100'}),
            'cash_payment_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_payment_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_receipt_heading': ('django.db.models.fields.CharField', [], {'default': "'Cash Receipt'", 'max_length': '100'}),
            'cash_receipt_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cash_receipt_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cheque_deposit_heading': ('django.db.models.fields.CharField', [], {'default': "'Cheque Deposit'", 'max_length': '100'}),
            'cheque_deposit_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cheque_deposit_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'cheque_payment_heading': ('django.db.models.fields.CharField', [], {'default': "'Cheque Payment'", 'max_length': '100'}),
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'voucher_settings'", 'unique': 'True', 'to': u"orm['users.Company']"}),
            'eft_in_heading': ('django.db.models.fields.CharField', [], {'default': "'EFT In'", 'max_length': '100'}),
            'eft_in_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'eft_in_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'eft_out_heading': ('django.db.models.fields.CharField', [], {'default': "'EFT Out'", 'max_length': '100'}),
            'fixed_assets_heading': ('django.db.models.fields.CharField', [], {'default': "'Fixed Assets Voucher'", 'max_length': '100'}),
            'fixed_assets_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'fixed_assets_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_heading': ('django.db.models.fields.CharField', [], {'default': "'Invoice'", 'max_length': '100'}),
            'invoice_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'invoice_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'journal_voucher_heading': ('django.db.models.fields.CharField', [], {'default': "'Journal Voucher'", 'max_length': '100'}),
            'journal_voucher_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'journal_voucher_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'physicalstock_heading': ('django.db.models.fields.CharField', [], {'default': "'Physical Stock Voucher'", 'max_length': '100'}),
            'physicalstock_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'physicalstock_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'purchase_voucher_heading': ('django.db.models.fields.CharField', [], {'default': "'Purchase Voucher'", 'max_length': '100'}),
            'purchase_voucher_prefix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'purchase_voucher_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'voucher_number_restart_days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'voucher_number_restart_months': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'voucher_number_restart_years': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'voucher_number_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['core']
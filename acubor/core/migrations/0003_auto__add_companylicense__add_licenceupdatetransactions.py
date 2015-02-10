# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CompanyLicense'
        db.create_table(u'core_companylicense', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.OneToOneField')(related_name='licence', unique=True, to=orm['users.Company'])),
            ('create_valid_from', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 1, 0, 0))),
            ('view_valid_from', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 1, 0, 0))),
            ('create_valid_to', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 31, 0, 0))),
            ('view_valid_to', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 8, 15, 0, 0))),
            ('last_updated_on', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 1, 0, 0))),
            ('last_updated_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], null=True)),
        ))
        db.send_create_signal(u'core', ['CompanyLicense'])

        # Adding model 'LicenceUpdateTransactions'
        db.create_table(u'core_licenceupdatetransactions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='licence_transactions', null=True, to=orm['users.Company'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('previous_create_licence_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('new_create_licence_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('previous_view_licence_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('new_view_licence_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('priced_amount', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='license_updates_performed', null=True, to=orm['users.User'])),
        ))
        db.send_create_signal(u'core', ['LicenceUpdateTransactions'])


    def backwards(self, orm):
        # Deleting model 'CompanyLicense'
        db.delete_table(u'core_companylicense')

        # Deleting model 'LicenceUpdateTransactions'
        db.delete_table(u'core_licenceupdatetransactions')


    models = {
        u'core.companylicense': {
            'Meta': {'object_name': 'CompanyLicense'},
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'licence'", 'unique': 'True', 'to': u"orm['users.Company']"}),
            'create_valid_from': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 1, 0, 0)'}),
            'create_valid_to': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 31, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'null': 'True'}),
            'last_updated_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 1, 0, 0)'}),
            'view_valid_from': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 1, 0, 0)'}),
            'view_valid_to': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 8, 15, 0, 0)'})
        },
        u'core.companysetting': {
            'Meta': {'object_name': 'CompanySetting'},
            'account_coding': ('django.db.models.fields.CharField', [], {'default': "'Automatic'", 'max_length': '9'}),
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'settings'", 'unique': 'True', 'to': u"orm['users.Company']"}),
            'decimal_places': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory_tracking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lotto_tracking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        u'core.licenceupdatetransactions': {
            'Meta': {'object_name': 'LicenceUpdateTransactions'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'licence_transactions'", 'null': 'True', 'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_create_licence_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'new_view_licence_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'previous_create_licence_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'previous_view_licence_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'priced_amount': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'license_updates_performed'", 'null': 'True', 'to': u"orm['users.User']"})
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
            'voucher_number_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 1, 0, 0)'})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User', 'db_table': "u'user'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 7, 1, 0, 0)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '245'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '245', 'null': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['core']
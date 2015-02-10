# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CompanyLicense'
        db.delete_table(u'core_companylicense')

        # Deleting model 'LicenceUpdateTransactions'
        db.delete_table(u'core_licenceupdatetransactions')

        # Adding field 'CompanySetting.company_type'
        db.add_column(u'core_companysetting', 'company_type',
                      self.gf('django.db.models.fields.CharField')(default='Gas Station and Store', max_length=50),
                      keep_default=False)

        # Adding field 'CompanySetting.financial_year_starts_on'
        db.add_column(u'core_companysetting', 'financial_year_starts_on',
                      self.gf('django.db.models.fields.CharField')(max_length=5, null=True),
                      keep_default=False)

        # Adding field 'CompanySetting.financial_year_ends_on'
        db.add_column(u'core_companysetting', 'financial_year_ends_on',
                      self.gf('django.db.models.fields.CharField')(max_length=5, null=True),
                      keep_default=False)

        # Adding field 'CompanySetting.current_financial_year_started_on'
        db.add_column(u'core_companysetting', 'current_financial_year_started_on',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 22, 0, 0)),
                      keep_default=False)

        # Adding field 'CompanySetting.registered_date'
        db.add_column(u'core_companysetting', 'registered_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 22, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'CompanyLicense'
        db.create_table(u'core_companylicense', (
            ('last_updated_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], null=True)),
            ('view_valid_from', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 1, 0, 0))),
            ('view_valid_to', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 8, 15, 0, 0))),
            ('create_valid_to', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 31, 0, 0))),
            ('create_valid_from', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 1, 0, 0))),
            ('company', self.gf('django.db.models.fields.related.OneToOneField')(related_name='licence', unique=True, to=orm['users.Company'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_updated_on', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 7, 1, 0, 0))),
        ))
        db.send_create_signal(u'core', ['CompanyLicense'])

        # Adding model 'LicenceUpdateTransactions'
        db.create_table(u'core_licenceupdatetransactions', (
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='license_updates_performed', null=True, to=orm['users.User'])),
            ('new_create_licence_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('previous_create_licence_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='licence_transactions', null=True, to=orm['users.Company'])),
            ('previous_view_licence_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_view_licence_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('priced_amount', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal(u'core', ['LicenceUpdateTransactions'])

        # Deleting field 'CompanySetting.company_type'
        db.delete_column(u'core_companysetting', 'company_type')

        # Deleting field 'CompanySetting.financial_year_starts_on'
        db.delete_column(u'core_companysetting', 'financial_year_starts_on')

        # Deleting field 'CompanySetting.financial_year_ends_on'
        db.delete_column(u'core_companysetting', 'financial_year_ends_on')

        # Deleting field 'CompanySetting.current_financial_year_started_on'
        db.delete_column(u'core_companysetting', 'current_financial_year_started_on')

        # Deleting field 'CompanySetting.registered_date'
        db.delete_column(u'core_companysetting', 'registered_date')


    models = {
        u'core.companysetting': {
            'Meta': {'object_name': 'CompanySetting'},
            'account_coding': ('django.db.models.fields.CharField', [], {'default': "'Automatic'", 'max_length': '9'}),
            'company': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'settings'", 'unique': 'True', 'to': u"orm['users.Company']"}),
            'company_type': ('django.db.models.fields.CharField', [], {'default': "'Gas Station and Store'", 'max_length': '50'}),
            'current_financial_year_started_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 22, 0, 0)'}),
            'decimal_places': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'financial_year_ends_on': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'financial_year_starts_on': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory_tracking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lotto_tracking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_comma_system': ('django.db.models.fields.CharField', [], {'default': "'120,000'", 'max_length': '8'}),
            'region_setting': ('django.db.models.fields.CharField', [], {'default': "'North America'", 'max_length': '15'}),
            'registered_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 22, 0, 0)'})
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
            'voucher_number_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 7, 22, 0, 0)'})
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
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ChequeDeposit', fields ['voucher_no', 'company']
        db.delete_unique(u'bank_chequedeposit', ['voucher_no', 'company_id'])

        # Removing unique constraint on 'BankCashDeposit', fields ['voucher_no', 'company']
        db.delete_unique(u'bank_bankcashdeposit', ['voucher_no', 'company_id'])

        # Removing unique constraint on 'ElectronicFundTransferIn', fields ['voucher_no', 'company']
        db.delete_unique(u'bank_electronicfundtransferin', ['voucher_no', 'company_id'])

        # Deleting model 'ChequeDepositRow'
        db.delete_table(u'bank_chequedepositrow')

        # Deleting model 'ElectronicFundTransferOut'
        db.delete_table(u'bank_electronicfundtransferout')

        # Deleting model 'ElectronicFundTransferIn'
        db.delete_table(u'bank_electronicfundtransferin')

        # Deleting model 'ChequePayment'
        db.delete_table(u'bank_chequepayment')

        # Deleting model 'ElectronicFundTransferInRow'
        db.delete_table(u'bank_electronicfundtransferinrow')

        # Deleting model 'BankCashDeposit'
        db.delete_table(u'bank_bankcashdeposit')

        # Deleting model 'ChequeDeposit'
        db.delete_table(u'bank_chequedeposit')


    def backwards(self, orm):
        # Adding model 'ChequeDepositRow'
        db.create_table(u'bank_chequedepositrow', (
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('drawee_bank_address', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('cheque_deposit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['bank.ChequeDeposit'])),
            ('cheque_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('cheque_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('drawee_bank', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'bank', ['ChequeDepositRow'])

        # Adding model 'ElectronicFundTransferOut'
        db.create_table(u'bank_electronicfundtransferout', (
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='electronic_fund_transfer_out', to=orm['ledger.Account'])),
            ('transaction_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('beneficiary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'bank', ['ElectronicFundTransferOut'])

        # Adding model 'ElectronicFundTransferIn'
        db.create_table(u'bank_electronicfundtransferin', (
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('benefactor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='electronic_fund_transfer_in', to=orm['ledger.Account'])),
        ))
        db.send_create_signal(u'bank', ['ElectronicFundTransferIn'])

        # Adding unique constraint on 'ElectronicFundTransferIn', fields ['voucher_no', 'company']
        db.create_unique(u'bank_electronicfundtransferin', ['voucher_no', 'company_id'])

        # Adding model 'ChequePayment'
        db.create_table(u'bank_chequepayment', (
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('cheque_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cheque_payments', to=orm['ledger.Account'])),
            ('beneficiary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'bank', ['ChequePayment'])

        # Adding model 'ElectronicFundTransferInRow'
        db.create_table(u'bank_electronicfundtransferinrow', (
            ('transaction_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('drawee_bank_address', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('transaction_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('electronic_fund_transfer_in', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['bank.ElectronicFundTransferIn'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('drawee_bank', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'bank', ['ElectronicFundTransferInRow'])

        # Adding model 'BankCashDeposit'
        db.create_table(u'bank_bankcashdeposit', (
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('benefactor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_deposits', to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('deposited_by', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'bank', ['BankCashDeposit'])

        # Adding unique constraint on 'BankCashDeposit', fields ['voucher_no', 'company']
        db.create_unique(u'bank_bankcashdeposit', ['voucher_no', 'company_id'])

        # Adding model 'ChequeDeposit'
        db.create_table(u'bank_chequedeposit', (
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('benefactor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cheque_deposits', to=orm['ledger.Account'])),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('deposited_by', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('clearing_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'bank', ['ChequeDeposit'])

        # Adding unique constraint on 'ChequeDeposit', fields ['voucher_no', 'company']
        db.create_unique(u'bank_chequedeposit', ['voucher_no', 'company_id'])


    models = {
        u'bank.bankaccount': {
            'Meta': {'object_name': 'BankAccount'},
            'ac_no': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ledger.Account']", 'unique': 'True'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'branch_name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'bank.bankdeposit': {
            'Meta': {'object_name': 'BankDeposit'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bank_deposit'", 'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'bank.bankdepositrow': {
            'Meta': {'object_name': 'BankDepositRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'bank_deposit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['bank.BankDeposit']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'from_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'bank.bankpayment': {
            'Meta': {'object_name': 'BankPayment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bank_payment'", 'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'bank.bankpaymentrow': {
            'Meta': {'object_name': 'BankPaymentRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'bank_payment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['bank.BankPayment']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'to_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"})
        },
        u'ledger.account': {
            'Meta': {'unique_together': "(('company', 'name'),)", 'object_name': 'Account'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts'", 'to': u"orm['ledger.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'current_cr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'current_dr': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_scheme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'account'", 'null': 'True', 'to': u"orm['ledger.InterestScheme']"}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'opening_as_on_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 9, 8, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'opening_cr': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'opening_dr': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['bank']
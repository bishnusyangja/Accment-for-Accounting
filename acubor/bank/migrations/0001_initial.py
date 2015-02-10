# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BankAccount'
        db.create_table(u'bank_bankaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('ac_no', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('branch_name', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ledger.Account'], unique=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'bank', ['BankAccount'])

        # Adding model 'ChequeDeposit'
        db.create_table(u'bank_chequedeposit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cheque_deposits', to=orm['ledger.Account'])),
            ('clearing_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('benefactor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('deposited_by', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'bank', ['ChequeDeposit'])

        # Adding unique constraint on 'ChequeDeposit', fields ['voucher_no', 'company']
        db.create_unique(u'bank_chequedeposit', ['voucher_no', 'company_id'])

        # Adding model 'ChequeDepositRow'
        db.create_table(u'bank_chequedepositrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('cheque_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('cheque_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('drawee_bank', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('drawee_bank_address', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('cheque_deposit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['bank.ChequeDeposit'])),
        ))
        db.send_create_signal(u'bank', ['ChequeDepositRow'])

        # Adding model 'BankCashDeposit'
        db.create_table(u'bank_bankcashdeposit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cash_deposits', to=orm['ledger.Account'])),
            ('benefactor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('deposited_by', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'bank', ['BankCashDeposit'])

        # Adding unique constraint on 'BankCashDeposit', fields ['voucher_no', 'company']
        db.create_unique(u'bank_bankcashdeposit', ['voucher_no', 'company_id'])

        # Adding model 'ChequePayment'
        db.create_table(u'bank_chequepayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cheque_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('beneficiary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cheque_payments', to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'bank', ['ChequePayment'])

        # Adding model 'ElectronicFundTransferOut'
        db.create_table(u'bank_electronicfundtransferout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('beneficiary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='electronic_fund_transfer_out', to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'bank', ['ElectronicFundTransferOut'])

        # Adding model 'ElectronicFundTransferIn'
        db.create_table(u'bank_electronicfundtransferin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='electronic_fund_transfer_in', to=orm['ledger.Account'])),
            ('benefactor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'bank', ['ElectronicFundTransferIn'])

        # Adding unique constraint on 'ElectronicFundTransferIn', fields ['voucher_no', 'company']
        db.create_unique(u'bank_electronicfundtransferin', ['voucher_no', 'company_id'])

        # Adding model 'ElectronicFundTransferInRow'
        db.create_table(u'bank_electronicfundtransferinrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.IntegerField')()),
            ('transaction_number', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('transaction_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('drawee_bank', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('drawee_bank_address', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('electronic_fund_transfer_in', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['bank.ElectronicFundTransferIn'])),
        ))
        db.send_create_signal(u'bank', ['ElectronicFundTransferInRow'])

        # Adding model 'BankDeposit'
        db.create_table(u'bank_bankdeposit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bank_deposit', to=orm['ledger.Account'])),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'bank', ['BankDeposit'])

        # Adding model 'BankDepositRow'
        db.create_table(u'bank_bankdepositrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('from_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('reference_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('bank_deposit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['bank.BankDeposit'])),
        ))
        db.send_create_signal(u'bank', ['BankDepositRow'])

        # Adding model 'BankPayment'
        db.create_table(u'bank_bankpayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voucher_no', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('bank_account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bank_payment', to=orm['ledger.Account'])),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('narration', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unapproved', max_length=10)),
        ))
        db.send_create_signal(u'bank', ['BankPayment'])

        # Adding model 'BankPaymentRow'
        db.create_table(u'bank_bankpaymentrow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('to_account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('reference_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('bank_payment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['bank.BankPayment'])),
        ))
        db.send_create_signal(u'bank', ['BankPaymentRow'])


    def backwards(self, orm):
        # Removing unique constraint on 'ElectronicFundTransferIn', fields ['voucher_no', 'company']
        db.delete_unique(u'bank_electronicfundtransferin', ['voucher_no', 'company_id'])

        # Removing unique constraint on 'BankCashDeposit', fields ['voucher_no', 'company']
        db.delete_unique(u'bank_bankcashdeposit', ['voucher_no', 'company_id'])

        # Removing unique constraint on 'ChequeDeposit', fields ['voucher_no', 'company']
        db.delete_unique(u'bank_chequedeposit', ['voucher_no', 'company_id'])

        # Deleting model 'BankAccount'
        db.delete_table(u'bank_bankaccount')

        # Deleting model 'ChequeDeposit'
        db.delete_table(u'bank_chequedeposit')

        # Deleting model 'ChequeDepositRow'
        db.delete_table(u'bank_chequedepositrow')

        # Deleting model 'BankCashDeposit'
        db.delete_table(u'bank_bankcashdeposit')

        # Deleting model 'ChequePayment'
        db.delete_table(u'bank_chequepayment')

        # Deleting model 'ElectronicFundTransferOut'
        db.delete_table(u'bank_electronicfundtransferout')

        # Deleting model 'ElectronicFundTransferIn'
        db.delete_table(u'bank_electronicfundtransferin')

        # Deleting model 'ElectronicFundTransferInRow'
        db.delete_table(u'bank_electronicfundtransferinrow')

        # Deleting model 'BankDeposit'
        db.delete_table(u'bank_bankdeposit')

        # Deleting model 'BankDepositRow'
        db.delete_table(u'bank_bankdepositrow')

        # Deleting model 'BankPayment'
        db.delete_table(u'bank_bankpayment')

        # Deleting model 'BankPaymentRow'
        db.delete_table(u'bank_bankpaymentrow')


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
        u'bank.bankcashdeposit': {
            'Meta': {'unique_together': "(('voucher_no', 'company'),)", 'object_name': 'BankCashDeposit'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_deposits'", 'to': u"orm['ledger.Account']"}),
            'benefactor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'deposited_by': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
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
        u'bank.chequedeposit': {
            'Meta': {'unique_together': "(('voucher_no', 'company'),)", 'object_name': 'ChequeDeposit'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cheque_deposits'", 'to': u"orm['ledger.Account']"}),
            'benefactor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'clearing_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'deposited_by': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'bank.chequedepositrow': {
            'Meta': {'object_name': 'ChequeDepositRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'cheque_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cheque_deposit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['bank.ChequeDeposit']"}),
            'cheque_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'drawee_bank': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'drawee_bank_address': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'bank.chequepayment': {
            'Meta': {'object_name': 'ChequePayment'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cheque_payments'", 'to': u"orm['ledger.Account']"}),
            'beneficiary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'cheque_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'})
        },
        u'bank.electronicfundtransferin': {
            'Meta': {'unique_together': "(('voucher_no', 'company'),)", 'object_name': 'ElectronicFundTransferIn'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'electronic_fund_transfer_in'", 'to': u"orm['ledger.Account']"}),
            'benefactor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'bank.electronicfundtransferinrow': {
            'Meta': {'object_name': 'ElectronicFundTransferInRow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'drawee_bank': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'drawee_bank_address': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'electronic_fund_transfer_in': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['bank.ElectronicFundTransferIn']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transaction_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'transaction_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'bank.electronicfundtransferout': {
            'Meta': {'object_name': 'ElectronicFundTransferOut'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'electronic_fund_transfer_out'", 'to': u"orm['ledger.Account']"}),
            'beneficiary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'narration': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'transaction_number': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['bank']
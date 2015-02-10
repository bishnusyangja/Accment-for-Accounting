# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('ledger_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['ledger.Category'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'ledger', ['Category'])

        # Adding unique constraint on 'Category', fields ['company', 'name']
        db.create_unique('ledger_category', ['company_id', 'name'])

        # Adding model 'Account'
        db.create_table(u'ledger_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('current_dr', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('current_cr', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='accounts', blank=True, to=orm['ledger.Category'])),
            ('opening_dr', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('opening_cr', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('opening_as_on_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('interest_scheme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='account', null=True, to=orm['ledger.InterestScheme'])),
        ))
        db.send_create_signal(u'ledger', ['Account'])

        # Adding unique constraint on 'Account', fields ['company', 'name']
        db.create_unique(u'ledger_account', ['company_id', 'name'])

        # Adding model 'TaxScheme'
        db.create_table(u'ledger_taxscheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('percent', self.gf('django.db.models.fields.FloatField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('collection_ledger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tax_scheme', null=True, to=orm['ledger.Account'])),
        ))
        db.send_create_signal(u'ledger', ['TaxScheme'])

        # Adding model 'InterestScheme'
        db.create_table(u'ledger_interestscheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('rate_in_pct', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'], null=True)),
            ('collection_ledger', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='int_scheme', null=True, to=orm['ledger.Account'])),
            ('interest_period', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'ledger', ['InterestScheme'])

        # Adding model 'BankAccountDetail'
        db.create_table(u'ledger_bankaccountdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='bank_detail', null=True, to=orm['ledger.Account'])),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('bank_address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('contact_no', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('bank_email_address', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'], null=True)),
        ))
        db.send_create_signal(u'ledger', ['BankAccountDetail'])

        # Adding model 'PartyAccountDetail'
        db.create_table(u'ledger_partyaccountdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='party_detail', null=True, to=orm['ledger.Account'])),
            ('party_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('party_address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('tin_no', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('party_email_address', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'], null=True)),
        ))
        db.send_create_signal(u'ledger', ['PartyAccountDetail'])

        # Adding model 'AccountTaxDetail'
        db.create_table(u'ledger_accounttaxdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tax_detail', null=True, to=orm['ledger.Account'])),
            ('pri_tax_scheme', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='primary_tax_scheme', null=True, to=orm['ledger.TaxScheme'])),
            ('sec_tax_scheme_1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='secondary_tax_scheme_1', null=True, to=orm['ledger.TaxScheme'])),
            ('sec_tax_scheme_2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='secondary_tax_scheme_2', null=True, to=orm['ledger.TaxScheme'])),
            ('sec_tax_scheme_3', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='secondary_tax_scheme_3', null=True, to=orm['ledger.TaxScheme'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'], null=True)),
        ))
        db.send_create_signal(u'ledger', ['AccountTaxDetail'])

        # Adding model 'JournalEntry'
        db.create_table(u'ledger_journalentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'ledger', ['JournalEntry'])

        # Adding model 'Transaction'
        db.create_table(u'ledger_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'])),
            ('dr_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cr_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('current_dr', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('current_cr', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('journal_entry', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', to=orm['ledger.JournalEntry'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'], null=True, blank=True)),
        ))
        db.send_create_signal(u'ledger', ['Transaction'])

        # Adding model 'Party'
        db.create_table('party', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Customer', max_length=17)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('customer_account', self.gf('django.db.models.fields.related.OneToOneField')(related_name='customer_detail', unique=True, null=True, to=orm['ledger.Account'])),
            ('supplier_account', self.gf('django.db.models.fields.related.OneToOneField')(related_name='supplier_detail', unique=True, null=True, to=orm['ledger.Account'])),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'ledger', ['Party'])


    def backwards(self, orm):
        # Removing unique constraint on 'Account', fields ['company', 'name']
        db.delete_unique(u'ledger_account', ['company_id', 'name'])

        # Removing unique constraint on 'Category', fields ['company', 'name']
        db.delete_unique('ledger_category', ['company_id', 'name'])

        # Deleting model 'Category'
        db.delete_table('ledger_category')

        # Deleting model 'Account'
        db.delete_table(u'ledger_account')

        # Deleting model 'TaxScheme'
        db.delete_table(u'ledger_taxscheme')

        # Deleting model 'InterestScheme'
        db.delete_table(u'ledger_interestscheme')

        # Deleting model 'BankAccountDetail'
        db.delete_table(u'ledger_bankaccountdetail')

        # Deleting model 'PartyAccountDetail'
        db.delete_table(u'ledger_partyaccountdetail')

        # Deleting model 'AccountTaxDetail'
        db.delete_table(u'ledger_accounttaxdetail')

        # Deleting model 'JournalEntry'
        db.delete_table(u'ledger_journalentry')

        # Deleting model 'Transaction'
        db.delete_table(u'ledger_transaction')

        # Deleting model 'Party'
        db.delete_table('party')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        u'ledger.accounttaxdetail': {
            'Meta': {'object_name': 'AccountTaxDetail'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tax_detail'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pri_tax_scheme': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary_tax_scheme'", 'null': 'True', 'to': u"orm['ledger.TaxScheme']"}),
            'sec_tax_scheme_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secondary_tax_scheme_1'", 'null': 'True', 'to': u"orm['ledger.TaxScheme']"}),
            'sec_tax_scheme_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secondary_tax_scheme_2'", 'null': 'True', 'to': u"orm['ledger.TaxScheme']"}),
            'sec_tax_scheme_3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secondary_tax_scheme_3'", 'null': 'True', 'to': u"orm['ledger.TaxScheme']"})
        },
        u'ledger.bankaccountdetail': {
            'Meta': {'object_name': 'BankAccountDetail'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bank_detail'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'bank_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'bank_email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']", 'null': 'True'}),
            'contact_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        u'ledger.journalentry': {
            'Meta': {'object_name': 'JournalEntry'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
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
        u'ledger.partyaccountdetail': {
            'Meta': {'object_name': 'PartyAccountDetail'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'party_detail'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'party_email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tin_no': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
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
        u'ledger.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']", 'null': 'True', 'blank': 'True'}),
            'cr_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'current_cr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'current_dr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dr_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal_entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'to': u"orm['ledger.JournalEntry']"})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['ledger']
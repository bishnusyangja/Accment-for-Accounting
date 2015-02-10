# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ScratchOffLatest.user'
        db.add_column(u'dayjournal_scratchofflatest', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='scratch_off_logs', null=True, to=orm['users.User']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ScratchOffLatest.user'
        db.delete_column(u'dayjournal_scratchofflatest', 'user_id')


    models = {
        u'dayjournal.bankattachment': {
            'Meta': {'object_name': 'BankAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bank_attachments'", 'to': u"orm['dayjournal.DayJournal']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.cardsales': {
            'Meta': {'object_name': 'CardSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'commission_out': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'card_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.cashequivalentsales': {
            'Meta': {'object_name': 'CashEquivalentSales'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_equivalent_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.cashsales': {
            'Meta': {'object_name': 'CashSales'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cash_sales'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sales_ledger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.dayjournal': {
            'Meta': {'unique_together': "(('voucher_no', 'company'),)", 'object_name': 'DayJournal', 'db_table': "'day_journal'"},
            'cash_actual': ('django.db.models.fields.FloatField', [], {}),
            'cash_deposit': ('django.db.models.fields.FloatField', [], {}),
            'cash_withdrawal': ('django.db.models.fields.FloatField', [], {}),
            'cheque_deposit': ('django.db.models.fields.FloatField', [], {}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lotto_sales_dispenser_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'lotto_sales_register_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'register_sales_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'register_sales_tax': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'scratch_off_sales_manual': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'scratch_off_sales_register_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.deposits': {
            'Meta': {'object_name': 'Deposits'},
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deposits'", 'to': u"orm['dayjournal.DayJournal']"}),
            'deposit_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deposit_from'", 'to': u"orm['ledger.Account']"}),
            'deposit_in': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deposit_in'", 'to': u"orm['ledger.Account']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.inventoryfuel': {
            'Meta': {'object_name': 'InventoryFuel'},
            'actual': ('django.db.models.fields.IntegerField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_fuel'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.InventoryAccount']"}),
            'purchase': ('django.db.models.fields.IntegerField', [], {}),
            'sales': ('django.db.models.fields.IntegerField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.lottodetail': {
            'Meta': {'object_name': 'LottoDetail'},
            'addition': ('django.db.models.fields.IntegerField', [], {}),
            'day_close': ('django.db.models.fields.IntegerField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lotto_detail'", 'to': u"orm['dayjournal.DayJournal']"}),
            'day_open': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pack_count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.otherattachment': {
            'Meta': {'object_name': 'OtherAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'other_attachments'", 'to': u"orm['dayjournal.DayJournal']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.otherpayout': {
            'Meta': {'object_name': 'OtherPayout'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'other_payout'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'paid_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'paid_for'", 'to': u"orm['ledger.Account']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.purchaseattachment': {
            'Meta': {'object_name': 'PurchaseAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_attachments'", 'to': u"orm['dayjournal.DayJournal']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.salesattachment': {
            'Meta': {'object_name': 'SalesAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sales_attachments'", 'to': u"orm['dayjournal.DayJournal']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dayjournal.scratchofflatest': {
            'Meta': {'object_name': 'ScratchOffLatest'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payroll.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_time': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'out_time': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scratch_off_logs'", 'null': 'True', 'to': u"orm['users.User']"})
        },
        u'dayjournal.scratchofflatestrow': {
            'Meta': {'object_name': 'ScratchOffLatestRow'},
            'addition': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_count': ('django.db.models.fields.FloatField', [], {}),
            'out_count': ('django.db.models.fields.FloatField', [], {}),
            'packet_count': ('django.db.models.fields.FloatField', [], {}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'scratch_off': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['dayjournal.ScratchOffLatest']"}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summaryinventory': {
            'Meta': {'object_name': 'SummaryInventory'},
            'actual': ('django.db.models.fields.IntegerField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_inventory'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.InventoryAccount']"}),
            'purchase': ('django.db.models.fields.IntegerField', [], {}),
            'sales': ('django.db.models.fields.IntegerField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dayjournal.summarytransfer': {
            'Meta': {'object_name': 'SummaryTransfer'},
            'cash': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'commission': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'summary_transfer'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'transfer_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"})
        },
        u'dayjournal.vendorcharge': {
            'Meta': {'object_name': 'VendorCharge'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vendor_charge'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_ledger': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'charges'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vendor_charge'", 'to': u"orm['ledger.Account']"})
        },
        u'dayjournal.vendorpayout': {
            'Meta': {'object_name': 'VendorPayout'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'day_journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vendor_payout'", 'to': u"orm['dayjournal.DayJournal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'purchase_ledger': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'payouts'", 'null': 'True', 'to': u"orm['ledger.Account']"}),
            'remarks': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '10'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vendor_payouts'", 'to': u"orm['ledger.Account']"})
        },
        u'inventory.inventoryaccount': {
            'Meta': {'object_name': 'InventoryAccount'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'opening_as_on_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 15, 0, 0)'}),
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
        u'payroll.employee': {
            'Meta': {'object_name': 'Employee'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ledger.Account']", 'unique': 'True', 'null': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'tax_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'null': 'True'})
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 15, 0, 0)'}),
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

    complete_apps = ['dayjournal']
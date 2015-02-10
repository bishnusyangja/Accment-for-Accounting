# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Invoice.party'
        db.alter_column('invoice', 'party_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Account'], null=True))

    def backwards(self, orm):

        # Changing field 'Invoice.party'
        db.alter_column('invoice', 'party_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ledger.Party'], null=True))

    models = {
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
            'opening_as_on_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 6, 0, 0)'}),
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
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']", 'null': 'True', 'blank': 'True'}),
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
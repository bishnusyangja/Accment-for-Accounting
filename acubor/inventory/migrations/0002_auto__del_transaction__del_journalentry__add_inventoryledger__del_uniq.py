# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Category', fields ['company', 'name']
        db.delete_unique(u'inventory_category', ['company_id', 'name'])

        # Deleting model 'Transaction'
        db.delete_table(u'inventory_transaction')

        # Deleting model 'JournalEntry'
        db.delete_table(u'inventory_journalentry')

        # Adding model 'InventoryLedger'
        db.create_table(u'inventory_inventoryledger', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inventory_transactions', null=True, to=orm['users.Company'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inventory_transactions', null=True, to=orm['inventory.InventoryAccount'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('rate', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal(u'inventory', ['InventoryLedger'])

        # Deleting field 'Item.purchase_account'
        db.delete_column(u'inventory_item', 'purchase_account_id')

        # Deleting field 'Item.code'
        db.delete_column(u'inventory_item', 'code')

        # Deleting field 'Item.purchase_tax_scheme'
        db.delete_column(u'inventory_item', 'purchase_tax_scheme_id')

        # Deleting field 'Item.sales_account'
        db.delete_column(u'inventory_item', 'sales_account_id')

        # Deleting field 'Item.sales_price'
        db.delete_column(u'inventory_item', 'sales_price')

        # Deleting field 'Item.purchase_price'
        db.delete_column(u'inventory_item', 'purchase_price')

        # Deleting field 'Item.sales_tax_scheme'
        db.delete_column(u'inventory_item', 'sales_tax_scheme_id')

        # Deleting field 'Item.current_stock'
        db.delete_column(u'inventory_item', 'current_stock')

        # Deleting field 'InventoryAccount.code'
        db.delete_column(u'inventory_inventoryaccount', 'code')

        # Deleting field 'InventoryAccount.current_dr'
        db.delete_column(u'inventory_inventoryaccount', 'current_dr')

        # Deleting field 'InventoryAccount.opening_balance'
        db.delete_column(u'inventory_inventoryaccount', 'opening_balance')

        # Deleting field 'InventoryAccount.current_cr'
        db.delete_column(u'inventory_inventoryaccount', 'current_cr')



    def backwards(self, orm):

        # Adding model 'Transaction'
        db.create_table(u'inventory_transaction', (
            ('dr_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.InventoryAccount'])),
            ('current_dr', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('journal_entry', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', to=orm['inventory.JournalEntry'])),
            ('cr_amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_cr', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Transaction'])

        # Adding model 'JournalEntry'
        db.create_table(u'inventory_journalentry', (
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('model_id', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inventory_journal_entries', to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal(u'inventory', ['JournalEntry'])

        # Deleting model 'InventoryLedger'
        db.delete_table(u'inventory_inventoryledger')

        # Adding unique constraint on 'Category', fields ['company', 'name']
        db.create_unique(u'inventory_category', ['company_id', 'name'])


        # User chose to not deal with backwards NULL issues for 'Item.purchase_account'
        raise RuntimeError("Cannot reverse this migration. 'Item.purchase_account' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Item.purchase_account'
        db.add_column(u'inventory_item', 'purchase_account',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchase_items', to=orm['ledger.Account']),
                      keep_default=False)

        # Adding field 'Item.code'
        db.add_column(u'inventory_item', 'code',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Item.purchase_tax_scheme'
        raise RuntimeError("Cannot reverse this migration. 'Item.purchase_tax_scheme' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Item.purchase_tax_scheme'
        db.add_column(u'inventory_item', 'purchase_tax_scheme',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='purchase_items', to=orm['ledger.TaxScheme']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Item.sales_account'
        raise RuntimeError("Cannot reverse this migration. 'Item.sales_account' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Item.sales_account'
        db.add_column(u'inventory_item', 'sales_account',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='sales_items', to=orm['ledger.Account']),
                      keep_default=False)

        # Adding field 'Item.sales_price'
        db.add_column(u'inventory_item', 'sales_price',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Item.purchase_price'
        db.add_column(u'inventory_item', 'purchase_price',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Item.sales_tax_scheme'
        raise RuntimeError("Cannot reverse this migration. 'Item.sales_tax_scheme' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Item.sales_tax_scheme'
        db.add_column(u'inventory_item', 'sales_tax_scheme',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='sales_items', to=orm['ledger.TaxScheme']),
                      keep_default=False)

        # Adding field 'Item.current_stock'
        db.add_column(u'inventory_item', 'current_stock',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'InventoryAccount.code'
        db.add_column(u'inventory_inventoryaccount', 'code',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'InventoryAccount.current_dr'
        db.add_column(u'inventory_inventoryaccount', 'current_dr',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'InventoryAccount.opening_balance'
        db.add_column(u'inventory_inventoryaccount', 'opening_balance',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'InventoryAccount.current_cr'
        db.add_column(u'inventory_inventoryaccount', 'current_cr',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'inventory.category': {
            'Meta': {'object_name': 'Category'},
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
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'inventory.inventoryledger': {
            'Meta': {'object_name': 'InventoryLedger'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_transactions'", 'null': 'True', 'to': u"orm['inventory.InventoryAccount']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_transactions'", 'null': 'True', 'to': u"orm['users.Company']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rate': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'inventory.item': {
            'Meta': {'object_name': 'Item'},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'item'", 'unique': 'True', 'to': u"orm['inventory.InventoryAccount']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items'", 'null': 'True', 'to': u"orm['inventory.Category']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_items'", 'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'opening_stock': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items'", 'null': 'True', 'to': u"orm['inventory.Unit']"})
        },
        u'inventory.physicalstockrow': {
            'Meta': {'object_name': 'PhysicalStockRow', 'db_table': "'physical_stock_row'"},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'physical_stock_voucher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'particulars'", 'to': u"orm['inventory.PhysicalStockVoucher']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'sn': ('django.db.models.fields.IntegerField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Unit']", 'null': 'True', 'blank': 'True'})
        },
        u'inventory.physicalstockvoucher': {
            'Meta': {'object_name': 'PhysicalStockVoucher', 'db_table': "'physical_stock_voucher'"},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'physical_stock_vouchers'", 'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'total_amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'voucher_no': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'inventory.unit': {
            'Meta': {'object_name': 'Unit'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_units'", 'to': u"orm['users.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'users.company': {
            'Meta': {'object_name': 'Company', 'db_table': "u'company'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        }
    }

    complete_apps = ['inventory']
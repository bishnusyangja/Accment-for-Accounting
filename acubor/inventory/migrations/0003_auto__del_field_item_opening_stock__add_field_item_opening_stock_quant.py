# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Item.opening_stock'
        db.delete_column(u'inventory_item', 'opening_stock')

        # Adding field 'Item.opening_stock_quantity'
        db.add_column(u'inventory_item', 'opening_stock_quantity',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Item.opening_stock'
        db.add_column(u'inventory_item', 'opening_stock',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Deleting field 'Item.opening_stock_quantity'
        db.delete_column(u'inventory_item', 'opening_stock_quantity')


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
            'opening_stock_quantity': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'items'", 'null': 'True', 'to': u"orm['inventory.Unit']"})
        },
        u'inventory.physicalstockrow': {
            'Meta': {'object_name': 'PhysicalStockRow', 'db_table': "'physical_stock_row'"},
            'amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Item']"}),
            'physical_stock_voucher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'particulars'", 'to': u"orm['inventory.PhysicalStockVoucher']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
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
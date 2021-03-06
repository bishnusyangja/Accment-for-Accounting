# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserPurchaseAttachment.uploaded_date'
        db.add_column(u'users_userpurchaseattachment', 'uploaded_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'UserPurchaseAttachment.processed_date'
        db.add_column(u'users_userpurchaseattachment', 'processed_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'UserPurchaseAttachment.is_processed'
        db.add_column(u'users_userpurchaseattachment', 'is_processed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserPurchaseAttachment.is_approved'
        db.add_column(u'users_userpurchaseattachment', 'is_approved',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserOtherAttachment.uploaded_date'
        db.add_column(u'users_userotherattachment', 'uploaded_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'UserOtherAttachment.processed_date'
        db.add_column(u'users_userotherattachment', 'processed_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'UserOtherAttachment.is_processed'
        db.add_column(u'users_userotherattachment', 'is_processed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserOtherAttachment.is_approved'
        db.add_column(u'users_userotherattachment', 'is_approved',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserSalesAttachment.uploaded_date'
        db.add_column(u'users_usersalesattachment', 'uploaded_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'UserSalesAttachment.processed_date'
        db.add_column(u'users_usersalesattachment', 'processed_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'UserSalesAttachment.is_processed'
        db.add_column(u'users_usersalesattachment', 'is_processed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserSalesAttachment.is_approved'
        db.add_column(u'users_usersalesattachment', 'is_approved',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserBankAttachment.uploaded_date'
        db.add_column(u'users_userbankattachment', 'uploaded_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'UserBankAttachment.processed_date'
        db.add_column(u'users_userbankattachment', 'processed_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'UserBankAttachment.is_processed'
        db.add_column(u'users_userbankattachment', 'is_processed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserBankAttachment.is_approved'
        db.add_column(u'users_userbankattachment', 'is_approved',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserPurchaseAttachment.uploaded_date'
        db.delete_column(u'users_userpurchaseattachment', 'uploaded_date')

        # Deleting field 'UserPurchaseAttachment.processed_date'
        db.delete_column(u'users_userpurchaseattachment', 'processed_date')

        # Deleting field 'UserPurchaseAttachment.is_processed'
        db.delete_column(u'users_userpurchaseattachment', 'is_processed')

        # Deleting field 'UserPurchaseAttachment.is_approved'
        db.delete_column(u'users_userpurchaseattachment', 'is_approved')

        # Deleting field 'UserOtherAttachment.uploaded_date'
        db.delete_column(u'users_userotherattachment', 'uploaded_date')

        # Deleting field 'UserOtherAttachment.processed_date'
        db.delete_column(u'users_userotherattachment', 'processed_date')

        # Deleting field 'UserOtherAttachment.is_processed'
        db.delete_column(u'users_userotherattachment', 'is_processed')

        # Deleting field 'UserOtherAttachment.is_approved'
        db.delete_column(u'users_userotherattachment', 'is_approved')

        # Deleting field 'UserSalesAttachment.uploaded_date'
        db.delete_column(u'users_usersalesattachment', 'uploaded_date')

        # Deleting field 'UserSalesAttachment.processed_date'
        db.delete_column(u'users_usersalesattachment', 'processed_date')

        # Deleting field 'UserSalesAttachment.is_processed'
        db.delete_column(u'users_usersalesattachment', 'is_processed')

        # Deleting field 'UserSalesAttachment.is_approved'
        db.delete_column(u'users_usersalesattachment', 'is_approved')

        # Deleting field 'UserBankAttachment.uploaded_date'
        db.delete_column(u'users_userbankattachment', 'uploaded_date')

        # Deleting field 'UserBankAttachment.processed_date'
        db.delete_column(u'users_userbankattachment', 'processed_date')

        # Deleting field 'UserBankAttachment.is_processed'
        db.delete_column(u'users_userbankattachment', 'is_processed')

        # Deleting field 'UserBankAttachment.is_approved'
        db.delete_column(u'users_userbankattachment', 'is_approved')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        },
        u'users.role': {
            'Meta': {'unique_together': "(('user', 'group', 'company'),)", 'object_name': 'Role'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['users.Company']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['users.User']"})
        },
        u'users.trackuserinfo': {
            'Meta': {'object_name': 'TrackUserInfo'},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddress': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'latitude': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'longitude': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User', 'db_table': "u'user'"},
            'currently_activated_company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']", 'null': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 1, 0, 0)'}),
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
        },
        u'users.userbankattachment': {
            'Meta': {'object_name': 'UserBankAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_bank_attachments'", 'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'processed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'uploaded_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'users.userotherattachment': {
            'Meta': {'object_name': 'UserOtherAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_other_attachments'", 'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'processed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'uploaded_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'users.userpurchaseattachment': {
            'Meta': {'object_name': 'UserPurchaseAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_purchase_attachments'", 'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'processed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'uploaded_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'users.usersalesattachment': {
            'Meta': {'object_name': 'UserSalesAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_sales_attachments'", 'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'processed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'uploaded_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['users']
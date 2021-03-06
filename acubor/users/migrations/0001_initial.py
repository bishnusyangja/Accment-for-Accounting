# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('location', self.gf('django.db.models.fields.TextField')()),
            ('type_of_business', self.gf('django.db.models.fields.CharField')(max_length=254)),
        ))
        db.send_create_signal(u'users', ['Company'])

        # Adding model 'User'
        db.create_table(u'user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=245)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=245, null=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 20, 0, 0))),
        ))
        db.send_create_signal(u'users', ['User'])

        # Adding model 'Role'
        db.create_table(u'users_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='roles', to=orm['users.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='roles', to=orm['auth.Group'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='roles', to=orm['users.Company'])),
        ))
        db.send_create_signal(u'users', ['Role'])

        # Adding unique constraint on 'Role', fields ['user', 'group', 'company']
        db.create_unique(u'users_role', ['user_id', 'group_id', 'company_id'])

        # Adding model 'UserSalesAttachment'
        db.create_table(u'users_usersalesattachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_sales_attachments', to=orm['users.Company'])),
        ))
        db.send_create_signal(u'users', ['UserSalesAttachment'])

        # Adding model 'UserPurchaseAttachment'
        db.create_table(u'users_userpurchaseattachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_purchase_attachments', to=orm['users.Company'])),
        ))
        db.send_create_signal(u'users', ['UserPurchaseAttachment'])

        # Adding model 'UserBankAttachment'
        db.create_table(u'users_userbankattachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_bank_attachments', to=orm['users.Company'])),
        ))
        db.send_create_signal(u'users', ['UserBankAttachment'])

        # Adding model 'UserOtherAttachment'
        db.create_table(u'users_userotherattachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_other_attachments', to=orm['users.Company'])),
        ))
        db.send_create_signal(u'users', ['UserOtherAttachment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Role', fields ['user', 'group', 'company']
        db.delete_unique(u'users_role', ['user_id', 'group_id', 'company_id'])

        # Deleting model 'Company'
        db.delete_table(u'company')

        # Deleting model 'User'
        db.delete_table(u'user')

        # Deleting model 'Role'
        db.delete_table(u'users_role')

        # Deleting model 'UserSalesAttachment'
        db.delete_table(u'users_usersalesattachment')

        # Deleting model 'UserPurchaseAttachment'
        db.delete_table(u'users_userpurchaseattachment')

        # Deleting model 'UserBankAttachment'
        db.delete_table(u'users_userbankattachment')

        # Deleting model 'UserOtherAttachment'
        db.delete_table(u'users_userotherattachment')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'type_of_business': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        },
        u'users.role': {
            'Meta': {'unique_together': "(('user', 'group', 'company'),)", 'object_name': 'Role'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['users.Company']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['users.User']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User', 'db_table': "u'user'"},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 20, 0, 0)'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'users.userotherattachment': {
            'Meta': {'object_name': 'UserOtherAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_other_attachments'", 'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'users.userpurchaseattachment': {
            'Meta': {'object_name': 'UserPurchaseAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_purchase_attachments'", 'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'users.usersalesattachment': {
            'Meta': {'object_name': 'UserSalesAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_sales_attachments'", 'to': u"orm['users.Company']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['users']
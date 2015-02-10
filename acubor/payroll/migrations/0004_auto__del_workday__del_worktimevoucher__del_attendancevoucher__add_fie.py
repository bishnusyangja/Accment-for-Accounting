# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'WorkDay'
        db.delete_table(u'payroll_workday')

        # Deleting model 'WorkTimeVoucher'
        db.delete_table(u'payroll_worktimevoucher')

        # Deleting model 'AttendanceVoucher'
        db.delete_table(u'payroll_attendancevoucher')

        # Adding field 'IndividualPayroll.worked_days'
        db.add_column(u'payroll_individualpayroll', 'worked_days',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'IndividualPayroll.worked_hours'
        db.add_column(u'payroll_individualpayroll', 'worked_hours',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'IndividualPayroll.worked_ot_hours'
        db.add_column(u'payroll_individualpayroll', 'worked_ot_hours',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'GroupPayrollRow.present_days'
        db.add_column(u'payroll_grouppayrollrow', 'present_days',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'GroupPayrollRow.present_hours'
        db.add_column(u'payroll_grouppayrollrow', 'present_hours',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'GroupPayrollRow.present_ot_hours'
        db.add_column(u'payroll_grouppayrollrow', 'present_ot_hours',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'WorkDay'
        db.create_table(u'payroll_workday', (
            ('in_time1', self.gf('django.db.models.fields.TextField')(default=None)),
            ('out_time1', self.gf('django.db.models.fields.TextField')(default=None)),
            ('out_time2', self.gf('django.db.models.fields.TextField')(default=None)),
            ('in_time2', self.gf('django.db.models.fields.TextField')(default=None)),
            ('day', self.gf('django.db.models.fields.DateField')(default=None)),
            ('work_time_voucher', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='work_days', to=orm['payroll.WorkTimeVoucher'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'payroll', ['WorkDay'])

        # Adding model 'WorkTimeVoucher'
        db.create_table(u'payroll_worktimevoucher', (
            ('voucher_no', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['payroll.Employee'])),
            ('from_date', self.gf('django.db.models.fields.DateField')(default=None)),
            ('to_date', self.gf('django.db.models.fields.DateField')(default=None)),
            ('date', self.gf('django.db.models.fields.DateField')(default=None)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['users.Company'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'payroll', ['WorkTimeVoucher'])

        # Adding model 'AttendanceVoucher'
        db.create_table(u'payroll_attendancevoucher', (
            ('half_multiplier', self.gf('django.db.models.fields.FloatField')(default=0.5, null=True, blank=True)),
            ('full_present_day', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Company'])),
            ('half_present_day', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['payroll.Employee'])),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('to_date', self.gf('django.db.models.fields.DateField')()),
            ('total_working_days', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('voucher_no', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('early_late_multiplier', self.gf('django.db.models.fields.FloatField')(default=1, null=True, blank=True)),
            ('early_late_attendance_day', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_ot_hours', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'payroll', ['AttendanceVoucher'])

        # Deleting field 'IndividualPayroll.worked_days'
        db.delete_column(u'payroll_individualpayroll', 'worked_days')

        # Deleting field 'IndividualPayroll.worked_hours'
        db.delete_column(u'payroll_individualpayroll', 'worked_hours')

        # Deleting field 'IndividualPayroll.worked_ot_hours'
        db.delete_column(u'payroll_individualpayroll', 'worked_ot_hours')

        # Deleting field 'GroupPayrollRow.present_days'
        db.delete_column(u'payroll_grouppayrollrow', 'present_days')

        # Deleting field 'GroupPayrollRow.present_hours'
        db.delete_column(u'payroll_grouppayrollrow', 'present_hours')

        # Deleting field 'GroupPayrollRow.present_ot_hours'
        db.delete_column(u'payroll_grouppayrollrow', 'present_ot_hours')


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
            'opening_as_on_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 17, 0, 0)'}),
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
        u'payroll.attendanceledger': {
            'Meta': {'unique_together': "(['employee', 'date'],)", 'object_name': 'AttendanceLedger'},
            'attendance_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attendance_ledger'", 'to': u"orm['payroll.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_time1': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'in_time2': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'out_time1': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'out_time2': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'payroll.deduction': {
            'Meta': {'object_name': 'Deduction'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_payroll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deductions'", 'to': u"orm['payroll.IndividualPayroll']"}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"})
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
        u'payroll.grouppayroll': {
            'Meta': {'object_name': 'GroupPayroll'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'payroll.grouppayrollrow': {
            'Meta': {'object_name': 'GroupPayrollRow'},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payroll.Employee']"}),
            'group_payroll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['payroll.GroupPayroll']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pay_head': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"}),
            'payroll_tax': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'present_days': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'present_hours': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'present_ot_hours': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rate_day': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rate_hour': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'rate_ot_hour': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'payroll.inclusion': {
            'Meta': {'object_name': 'Inclusion'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_payroll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inclusions'", 'to': u"orm['payroll.IndividualPayroll']"}),
            'particular': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ledger.Account']"})
        },
        u'payroll.individualpayroll': {
            'Meta': {'object_name': 'IndividualPayroll'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payroll.Employee']"}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            'hour_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ot_hour_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unapproved'", 'max_length': '10'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'worked_days': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'worked_hours': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'worked_ot_hours': ('django.db.models.fields.FloatField', [], {'null': 'True'})
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 17, 0, 0)'}),
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

    complete_apps = ['payroll']
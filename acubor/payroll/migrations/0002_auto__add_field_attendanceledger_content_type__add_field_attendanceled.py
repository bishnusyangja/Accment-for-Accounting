# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AttendanceLedger.content_type'
        db.add_column(u'payroll_attendanceledger', 'content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=72, to=orm['contenttypes.ContentType']),
                      keep_default=False)

        # Adding field 'AttendanceLedger.object_id'
        db.add_column(u'payroll_attendanceledger', 'object_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'AttendanceLedger.content_type'
        db.delete_column(u'payroll_attendanceledger', 'content_type_id')

        # Deleting field 'AttendanceLedger.object_id'
        db.delete_column(u'payroll_attendanceledger', 'object_id')


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
            'opening_as_on_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
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
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '72', 'to': u"orm['contenttypes.ContentType']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attendance_ledger'", 'to': u"orm['payroll.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_time1': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'in_time2': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'out_time1': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'out_time2': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'payroll.attendancevoucher': {
            'Meta': {'object_name': 'AttendanceVoucher'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'early_late_attendance_day': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'early_late_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payroll.Employee']"}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            'full_present_day': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'half_multiplier': ('django.db.models.fields.FloatField', [], {'default': '0.5', 'null': 'True', 'blank': 'True'}),
            'half_present_day': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'total_ot_hours': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_working_days': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'payroll.workday': {
            'Meta': {'object_name': 'WorkDay'},
            'day': ('django.db.models.fields.DateField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_time1': ('django.db.models.fields.TextField', [], {'default': 'None'}),
            'in_time2': ('django.db.models.fields.TextField', [], {'default': 'None'}),
            'out_time1': ('django.db.models.fields.TextField', [], {'default': 'None'}),
            'out_time2': ('django.db.models.fields.TextField', [], {'default': 'None'}),
            'work_time_voucher': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'work_days'", 'to': u"orm['payroll.WorkTimeVoucher']"})
        },
        u'payroll.worktimevoucher': {
            'Meta': {'object_name': 'WorkTimeVoucher'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['users.Company']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'None'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['payroll.Employee']"}),
            'from_date': ('django.db.models.fields.DateField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_date': ('django.db.models.fields.DateField', [], {'default': 'None'}),
            'voucher_no': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
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
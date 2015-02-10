from rest_framework import serializers

from payroll.models import Employee, GroupPayroll, GroupPayrollRow, \
    IndividualPayroll, Inclusion, AttendanceLedger, AttendanceParameter


class AttendanceParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceParameter


class EmployeeSerializer(serializers.ModelSerializer):
    #text = serializers.Field(source='name')
    # unpaid_days = serializers.Field(source='get_unpaid_days')
    # unpaid_hours = serializers.Field(source='get_unpaid_hours')
    # unpaid_ot_hours = serializers.Field(source='get_unpaid_ot_hours')

    class Meta:
        model = Employee
        # fields = ['name', 'id', 'tax_id', 'unpaid_days', 'unpaid_hours', 'unpaid_ot_hours']


# class AttendanceVoucherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AttendanceVoucher
#         exclude = ['company']


# class WorkDaySerializer(serializers.ModelSerializer):
#     in_time1 = serializers.Field(source='get_in_time1')
#     out_time1 = serializers.Field(source='get_out_time1')
#     in_time2 = serializers.Field(source='get_in_time2')
#     out_time2 = serializers.Field(source='get_out_time2')
#
#     class Meta:
#         model = WorkDay
#         exclude = ['work_time_voucher']


# class WorkTimeVoucherRowSerializer(serializers.ModelSerializer):
#     work_days = WorkDaySerializer()
#
#     class Meta:
#         model = WorkTimeVoucherRow
#         exclude = ['work_time_voucher']


# class WorkTimeVoucherSerializer(serializers.ModelSerializer):
#     work_days = WorkDaySerializer()
#
#     class Meta:
#         model = WorkTimeVoucher
#         exclude = ['company']


class GroupPayrollRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPayrollRow


class GroupPayrollSerializer(serializers.ModelSerializer):
    rows = GroupPayrollRowSerializer()

    class Meta:
        model = GroupPayroll


class InclusionSerializer(serializers.ModelSerializer):
    account = serializers.Field(source='particular.id')

    class Meta:
        model = Inclusion


class DeductionSerializer(serializers.ModelSerializer):
    account = serializers.Field(source='particular.id')

    class Meta:
        model = Inclusion


class IndividualPayrollSerializer(serializers.ModelSerializer):
    inclusions = InclusionSerializer()
    deductions = DeductionSerializer()

    class Meta:
        model = IndividualPayroll


class AttendanceLedgerSerializer(serializers.ModelSerializer):
    date = serializers.Field(source='get_date')
    in_time1 = serializers.Field(source='get_in_time1')
    out_time1 = serializers.Field(source='get_out_time1')
    in_time2 = serializers.Field(source='get_in_time2')
    out_time2 = serializers.Field(source='get_out_time2')

    class Meta:
        model = AttendanceLedger

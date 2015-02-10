from django.db import models
from django.db.models import Max

from lib import zero_for_none
from ledger.models import Account, JournalEntry, set_transactions
from users.models import Company, User
import json
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from ledger.models import Transaction


class Employee(models.Model):
    name = models.CharField(max_length=254, verbose_name='Name *')
    address = models.TextField(null=True, blank=True)
    tax_id = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    account = models.OneToOneField(Account, null=True)
    company = models.ForeignKey(Company)
    user = models.ForeignKey(User, blank=True, null=True)

    def set_paid(self, start, end):
        attendance_ledgers = AttendanceLedger.objects.filter(employee=self, paid=False, date__range=(start, end))
        for ledger in attendance_ledgers:
            ledger.paid = True
            ledger.save()

    def set_unpaid(self, start, end):
        attendance_ledgers = AttendanceLedger.objects.filter(employee=self, paid=True, date__range=(start, end))
        for ledger in attendance_ledgers:
            ledger.paid = False
            ledger.save()

    def get_worked_hours(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end)
        total = 0
        for ledger in attendance_ledger:
            total += ledger.get_worked_minutes()
        return round(total/60.0, 2)

    def get_unpaid_worked_hours(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end, paid=False)
        total = 0
        for ledger in attendance_ledger:
            total += ledger.get_worked_minutes()
        return round(total/60.0, 2)

    def get_full_attendance_day(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end,
                                                            attendance_status='Full Attendance')
        return len(attendance_ledger)

    def get_unpaid_full_attendance_day(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end,
                                                                attendance_status='Full Attendance', paid=False)
        return len(attendance_ledger)

    def get_late_attendance_day(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end,
                                                            attendance_status='Late Attendance')
        return len(attendance_ledger)

    def get_unpaid_late_attendance_day(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end,
                                                            attendance_status='Late Attendance', paid=False)
        return len(attendance_ledger)

    def get_half_attendance_day(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end,
                                                            attendance_status='Half Attendance')
        return len(attendance_ledger)

    def get_unpaid_half_attendance_day(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end,
                                                            attendance_status='Half Attendance', paid=False)
        return len(attendance_ledger)

    def get_early_leave_day(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end,
                                                            attendance_status='Early Leave')
        return len(attendance_ledger)

    def get_unpaid_early_leave_day(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end,
                                                            attendance_status='Early Leave', paid=False)
        return len(attendance_ledger)

    def get_absent_day(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__gte=start, date__lte=end,
                                                            attendance_status='Absent')
        return len(attendance_ledger)

    def get_unpaid_absent_day(self, start, end):
        attendance_ledger = AttendanceLedger.objects.filter(employee=self, date__range=(start, end), attendance_status='Absent')
        return len(attendance_ledger)

    def get_worked_days(self, start, end):
        return self.get_full_attendance_day(start, end) + 0.5*(self.get_late_attendance_day(start, end) + self.get_early_leave_day(start, end) + self.get_half_attendance_day(start, end))

    def get_unpaid_worked_days(self, start, end):
        obj = AttendanceParameter.objects.filter(company=self.company)[0]
        full_att = 1 if not obj else obj.full_att
        late_att = 0.33 if not obj else obj.late_att
        half_att = 0.5 if not obj else obj.half_att
        early_leave = 0.33 if not obj else obj.early_leave

        result = full_att*self.get_unpaid_full_attendance_day(start, end) + late_att*self.get_unpaid_late_attendance_day(start, end) + \
                early_leave*self.get_unpaid_early_leave_day(start, end) + half_att*self.get_unpaid_half_attendance_day(start, end)
        return round(result, 2)

    def __str__(self):
        return self.name


class GroupPayroll(models.Model):
    voucher_no = models.CharField(max_length=50)
    date = models.DateField()
    from_date = models.DateField()
    to_date = models.DateField()
    company = models.ForeignKey(Company)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __str__(self):
        return 'Group Payroll at ' + str(self.date)

    def get_absolute_url(self):
        return '/payroll/group-voucher/' + str(self.id)

    def get_wt_voucher_no(self, request):
        num = GroupPayroll.objects.filter(company=request.user.currently_activated_company).aggregate(Max('voucher_no'))['voucher_no__max']
        if num is None:
            num = 0
        return int(num) + 1

    def get_voucher_no(self):
        return self.voucher_no

    def get_company(self):
        return self.company

    def backend_approve(self, request):
        payroll_tax = Account.objects.get(name='Payroll Tax', company=request.user.currently_activated_company)
        for row in self.rows.all():
            amount = row.rate_day * row.employee.get_unpaid_worked_days(self.from_date, self.to_date) + row.rate_hour * row.employee.get_unpaid_worked_hours(self.from_date, self.to_date)
            net_amount = amount - row.payroll_tax
            if net_amount >= 0:
                set_transactions(row, self.date,
                                 ['dr', row.pay_head, amount],
                                 ['cr', payroll_tax, row.payroll_tax],
                                 ['cr', row.employee.account, net_amount])
            else:
                set_transactions(row, self.date,
                                 ['dr', row.pay_head, amount],
                                 ['cr', payroll_tax, row.payroll_tax],
                                 ['dr', row.employee.account, net_amount*(-1)])
            row.employee.set_paid(self.from_date, self.to_date)

        self.status = 'Approved'
        self.save()

    def backend_unapprove(self):
        ctype = ContentType.objects.get(model='grouppayrollrow')
        for row in self.rows.all():
            entries = JournalEntry.objects.filter(content_type=ctype, object_id=row.id)
            for entry in entries:
                entry.delete()
        self.status = 'Unapproved'
        self.save()
        for row in self.rows.all():
            row.employee.set_unpaid(self.from_date, self.to_date)


class GroupPayrollRow(models.Model):
    employee = models.ForeignKey(Employee)
    rate_day = models.FloatField(null=True, blank=True)
    rate_hour = models.FloatField(null=True, blank=True)
    rate_ot_hour = models.FloatField(null=True, blank=True)
    payroll_tax = models.FloatField(null=True, blank=True)
    pay_head = models.ForeignKey(Account)
    present_days = models.FloatField(null=True)
    present_hours = models.FloatField(null=True)
    present_ot_hours = models.FloatField(null=True)
    group_payroll = models.ForeignKey(GroupPayroll, related_name='rows')

    def get_voucher_description(self):
        return ''

    def get_voucher_no(self):
        return self.group_payroll.get_voucher_no()

    def get_absolute_url(self):
        return self.group_payroll.get_absolute_url()

    def get_company(self):
        return self.group_payroll.company

    def get_worked_days(self):
        obj = AttendanceParameter.objects.filter(company=self.employee.company)[0]
        full_att = 1 if not obj else obj.full_att
        late_att = 0.33 if not obj else obj.late_att
        half_att = 0.5 if not obj else obj.half_att
        early = 0.33 if not obj else obj.early_leave
        ledger = AttendanceLedger.objects.filter(employee=self.employee, date__lte=self.group_payroll.to_date, date__gte=self.group_payroll.from_date)
        full_attendance = ledger.filter(attendance_status='Full Attendance')
        late_attendance = ledger.filter(attendance_status='Late Attendance')
        half_attendance = ledger.filter(attendance_status='Half Attendance')
        early_leave = ledger.filter(attendance_status='Early Leave')
        result = full_att*len(full_attendance) + late_att*len(late_attendance) + half_att*len(half_attendance) + early*len(early_leave)
        return round(result, 2)

    def get_worked_hours(self):
        ledger = AttendanceLedger.objects.filter(employee=self.employee, date__lte=self.group_payroll.to_date, date__gte=self.group_payroll.from_date)
        total = 0
        for item in ledger:
            total += item.get_worked_minutes()
        return round(total/60.0, 2)


class IndividualPayroll(models.Model):
    employee = models.ForeignKey(Employee)
    voucher_no = models.CharField(max_length=50)
    date = models.DateField()
    from_date = models.DateField()
    to_date = models.DateField()
    company = models.ForeignKey(Company)
    day_rate = models.FloatField(null=True, blank=True)
    hour_rate = models.FloatField(null=True, blank=True)
    ot_hour_rate = models.FloatField(null=True, blank=True)
    days_worked = models.FloatField(null=True)
    hours_worked = models.FloatField(null=True)
    ot_hours_worked = models.FloatField(null=True)
    statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    status = models.CharField(max_length=10, choices=statuses, default='Unapproved')

    def __str__(self):
        return 'Individual Payroll at ' + str(self.date)

    def get_absolute_url(self):
        return '/payroll/individual-voucher/' + str(self.id)

    def get_wt_voucher_no(self, request):
        num = IndividualPayroll.objects.filter(company=request.user.currently_activated_company).aggregate(Max('voucher_no'))['voucher_no__max']
        if num is None:
            num = 0
        return int(num) + 1

    def get_voucher_no(self):
        return self.voucher_no

    def get_total_payable_amt(self, start, end):
        total = 0
        total = total + zero_for_none(self.employee.get_unpaid_worked_days(start, end)) * zero_for_none(self.day_rate)
        total = total + zero_for_none(self.employee.get_unpaid_worked_hours(start, end)) * zero_for_none(self.hour_rate)
        # total = total + zero_for_none(self.employee.get_unpaid_worked_ot_hours()) * zero_for_none(self.ot_hour_rate)
        return total

    def get_voucher_description(self):
        return ""

    def get_company(self):
        return self.company

    def backend_approve(self, request):
        total_salary = self.get_total_payable_amt(self.from_date, self.to_date)
        salary_account = Account.objects.get(company=request.user.currently_activated_company, name='Salary')
        # this object is not found here and is .....
        ctype = ContentType.objects.get_for_model(self)
        journal_entry = JournalEntry(date=self.date, content_type=ctype, object_id=self.id, company=self.company)
        journal_entry.save()

        if zero_for_none(total_salary) > 0:
            transaction = Transaction(account=salary_account, dr_amount=total_salary, cr_amount=0, company=self.company,
                                      journal_entry=journal_entry)
            transaction.save()
        elif zero_for_none(total_salary) < 0:
            transaction = Transaction(account=salary_account, cr_amount=abs(total_salary), dr_amount=0,
                                      company=self.company, journal_entry=journal_entry)
            transaction.save()

        total_inclusion = 0
        for row in self.inclusions.all():
            if zero_for_none(row.amount) > 0:
                transaction = Transaction(account=row.particular, dr_amount=row.amount, cr_amount=0,
                                          company=self.company, journal_entry=journal_entry)
                transaction.save()
            if zero_for_none(row.amount) < 0:
                transaction = Transaction(account=row.particular, cr_amount=row.amount, dr_amount=0,
                                          company=self.company, journal_entry=journal_entry)
                transaction.save()
            total_inclusion += row.amount

        total_exclusion = 0
        for row in self.deductions.all():
            if zero_for_none(row.amount) > 0:
                transaction = Transaction(account=row.particular, cr_amount=row.amount, dr_amount=0,
                                          company=self.company, journal_entry=journal_entry)
                transaction.save()
            elif zero_for_none(row.amount) < 0:
                transaction = Transaction(account=row.particular, dr_amount=row.amount, cr_amount=0,
                                          company=self.company, journal_entry=journal_entry)
                transaction.save()
            total_exclusion += row.amount

        diff = total_salary + total_inclusion - total_exclusion
        if diff > 0:
            transaction = Transaction(account=self.employee.account, cr_amount=diff, dr_amount=0,
                                      company=self.company, journal_entry=journal_entry)
            transaction.save()
        elif diff < 0:
            transaction = Transaction(account=self.employee.account, dr_amount=abs(diff), cr_amount=0,
                                      company=self.company, journal_entry=journal_entry)
            transaction.save()

        self.employee.set_paid(self.from_date, self.to_date)
        self.status = 'Approved'
        self.save()

    def backend_unapprove(self):
        ctype = ContentType.objects.get(model='individualpayroll')
        entries = JournalEntry.objects.filter(content_type=ctype, object_id=self.id)
        for entry in entries:
            entry.delete()
        self.status = 'Unapproved'
        self.save()
        self.employee.set_unpaid(self.from_date, self.to_date)

    def get_worked_days(self):
        obj = AttendanceParameter.objects.filter(company=self.employee.company)[0]
        full_att = 1 if not obj else obj.full_att
        late_att = 0.33 if not obj else obj.late_att
        half_att = 0.5 if not obj else obj.half_att
        early = 0.33 if not obj else obj.early_leave
        ledger = AttendanceLedger.objects.filter(employee=self.employee, date__lte=self.to_date, date__gte=self.from_date)
        full_attendance = ledger.filter(attendance_status='Full Attendance')
        late_attendance = ledger.filter(attendance_status='Late Attendance')
        half_attendance = ledger.filter(attendance_status='Half Attendance')
        early_leave = ledger.filter(attendance_status='Early Leave')
        result = full_att*len(full_attendance) + late_att*len(late_attendance) + half_att*len(half_attendance) + early*len(early_leave)
        return round(result, 2)

    def get_worked_hours(self):
        ledger = AttendanceLedger.objects.filter(employee=self.employee, date__lte=self.to_date, date__gte=self.from_date)
        total = 0
        for item in ledger:
            total += item.get_worked_minutes()
        return round(total/60.0, 2)


class Inclusion(models.Model):
    particular = models.ForeignKey(Account)
    amount = models.FloatField()
    individual_payroll = models.ForeignKey(IndividualPayroll, related_name='inclusions')

    def get_absolute_url(self):
        return self.individual_payroll.get_absolute_url()

    def get_voucher_description(self):
        return ''

    def get_company(self):
        return self.individual_payroll.company

    def get_voucher_no(self):
        return self.individual_payroll.voucher_no


class Deduction(models.Model):
    particular = models.ForeignKey(Account)
    amount = models.FloatField()
    individual_payroll = models.ForeignKey(IndividualPayroll, related_name='deductions')

    def get_absolute_url(self):
        return self.individual_payroll.get_absolute_url()

    def get_voucher_description(self):
        return ''

    def get_company(self):
        return self.individual_payroll.company

    def get_voucher_no(self):
        return self.individual_payroll.voucher_no


# the latest model for attendance voucher is here where both hour attendance and day attendance is in the same voucher
class AttendanceLedger(models.Model):
    employee = models.ForeignKey(Employee, related_name='attendance_ledger')
    date = models.DateField()
    in_time1 = models.TimeField(null=True, blank=True)
    out_time1 = models.TimeField(null=True, blank=True)
    in_time2 = models.TimeField(null=True, blank=True)
    out_time2 = models.TimeField(null=True, blank=True)
    attendance_statuses = [('FA', 'Full Attendance'),('LA','Late Attendance'),('HA', 'Half Attendance'),('EL', 'Early Leave'),('A', 'Absent')]
    attendance_status = models.CharField(max_length=20, choices=attendance_statuses, null=True, blank=True)
    paid = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def get_date(self):
        date = str(self.date)
        s_date = date.split('-')
        return s_date[1] + '/' + s_date[2] + '/' + s_date[0]

    def get_in_time1(self):
        return hr_12(self.in_time1)

    def get_in_time2(self):
        return  hr_12(self.in_time2)

    def get_out_time1(self):
        return hr_12(self.out_time1)

    def get_out_time2(self):
        return hr_12(self.out_time2)

    def get_worked_minutes(self):
        if self.in_time1:
            first_half = sub_time(self.in_time1, self.out_time1)
        else:
            first_half = 0
        if self.in_time2:
            second_half = sub_time(self.in_time2, self.out_time2)
        else:
            second_half = 0
        return first_half + second_half

    class Meta:
        unique_together = ['employee', 'date']

    def __str__(self):
        return str(self.date) + str(self.employee)


# subtracting two time field of django
def sub_time(a, b):
    hour = b.hour - a.hour
    hour = 12 + hour if hour < 0 else hour
    minute = b.minute - a.minute
    minute = 60 + minute if minute < 0 else minute
    return hour*60 + minute


# getting the 12 hour format of the django time field
def hr_12(value):
    if value is not None:
        value = str(value)
        lis = value.split(':')
        h = int(lis[0])
        m = int(lis[1])
        if h >= 12:
            h -= 12
            return str(h) + ':' + str(m) + ' PM'
        elif h == 00:
            return '12:' + str(m) + ' AM'
        else:
            return str(h) + ':' + str(m) + ' AM'
    else:
        return value


# this model class is for attendance parameter
class AttendanceParameter(models.Model):
    full_att = models.FloatField(default=1.0, verbose_name='Full Attendance Factor')
    late_att = models.FloatField(default=0.66, verbose_name='Late Attendance Factor')
    half_att = models.FloatField(default=0.5, verbose_name='Half Attendance Factor')
    early_leave = models.FloatField(default=0.66, verbose_name='Early Leave Factor')
    abs = models.FloatField(default=0.0, verbose_name='Absent Factor')
    company = models.ForeignKey(Company, null=True, blank=True)
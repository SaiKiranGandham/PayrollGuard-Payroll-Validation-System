
from django.db import models
from employees.models import Employee


class PayGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    payment_frequency = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PayPeriod(models.Model):
    pay_group = models.ForeignKey(
        PayGroup,
        on_delete=models.PROTECT,
        related_name="pay_periods"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    payment_date = models.DateField()
    status = models.CharField(max_length=20, default="DRAFT")

    class Meta:
        ordering = ["-start_date"]
        unique_together = ("pay_group", "start_date", "end_date")

    def __str__(self):
        return f"{self.pay_group.name}: {self.start_date} to {self.end_date}"


class TimeEntry(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    pay_period = models.ForeignKey(PayPeriod, on_delete=models.PROTECT)
    work_date = models.DateField()
    regular_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    approval_status = models.CharField(max_length=20, default="PENDING")

    def __str__(self):
        return f"{self.employee.employee_id} - {self.work_date}"


class LeaveRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    pay_period = models.ForeignKey(PayPeriod, on_delete=models.PROTECT)
    leave_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_days = models.DecimalField(max_digits=5, decimal_places=2)
    approval_status = models.CharField(max_length=20, default="PENDING")

    def __str__(self):
        return f"{self.employee.employee_id} - {self.leave_type}"


class Allowance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    pay_period = models.ForeignKey(PayPeriod, on_delete=models.PROTECT)
    allowance_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    approval_status = models.CharField(max_length=20, default="PENDING")

    def __str__(self):
        return f"{self.employee.employee_id} - {self.allowance_type}"


class Deduction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    pay_period = models.ForeignKey(PayPeriod, on_delete=models.PROTECT)
    deduction_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    approval_status = models.CharField(max_length=20, default="PENDING")

    def __str__(self):
        return f"{self.employee.employee_id} - {self.deduction_type}"


class PayrollInput(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    pay_period = models.ForeignKey(PayPeriod, on_delete=models.PROTECT)

    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    total_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    gross_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, default="DRAFT")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("employee", "pay_period")

    def __str__(self):
        return f"{self.employee.employee_id} - Payroll"

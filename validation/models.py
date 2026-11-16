from django.db import models

# Create your models here.

from django.db import models
from employees.models import Employee
from payroll.models import PayPeriod, PayrollInput


class ValidationRule(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    rule_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20, default="ERROR")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Exception(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT
    )
    pay_period = models.ForeignKey(
        PayPeriod,
        on_delete=models.PROTECT
    )
    payroll_input = models.ForeignKey(
        PayrollInput,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    validation_rule = models.ForeignKey(
        ValidationRule,
        on_delete=models.PROTECT
    )

    description = models.TextField()
    severity = models.CharField(max_length=20, default="ERROR")
    status = models.CharField(max_length=20, default="OPEN")
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.employee_id} - {self.validation_rule.name}"

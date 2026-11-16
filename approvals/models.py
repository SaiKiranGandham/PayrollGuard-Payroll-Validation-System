

from django.db import models
from django.conf import settings
from employees.models import Employee
from payroll.models import PayPeriod, PayrollInput


class Approval(models.Model):
    payroll_input = models.ForeignKey(
        PayrollInput,
        on_delete=models.PROTECT
    )
    approver = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT
    )
    status = models.CharField(max_length=20, default="PENDING")
    comments = models.TextField(blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Approval - {self.payroll_input}"


class PayrollExport(models.Model):
    pay_period = models.ForeignKey(
        PayPeriod,
        on_delete=models.PROTECT
    )
    file_name = models.CharField(max_length=255)
    export_format = models.CharField(max_length=20, default="CSV")
    status = models.CharField(max_length=20, default="PENDING")
    exported_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name


class ApprovalEvent(models.Model):
    approval = models.ForeignKey(
        Approval,
        on_delete=models.PROTECT,
        related_name="events"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    event_type = models.CharField(max_length=50)
    previous_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} - {self.approval_id}"


from django.contrib import admin
from .models import Approval, PayrollExport, ApprovalEvent


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = (
        "payroll_input",
        "approver",
        "status",
        "approved_at",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("payroll_input__employee__employee_id",)


@admin.register(PayrollExport)
class PayrollExportAdmin(admin.ModelAdmin):
    list_display = (
        "file_name",
        "pay_period",
        "export_format",
        "status",
        "exported_at",
    )
    list_filter = ("export_format", "status")
    search_fields = ("file_name",)


@admin.register(ApprovalEvent)
class ApprovalEventAdmin(admin.ModelAdmin):
    list_display = (
        "approval",
        "event_type",
        "previous_status",
        "new_status",
        "created_at",
    )
    list_filter = ("event_type", "new_status")

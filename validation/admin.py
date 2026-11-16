
from django.contrib import admin
from .models import ValidationRule, Exception


@admin.register(ValidationRule)
class ValidationRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "rule_type", "severity", "is_active")
    search_fields = ("name", "description")
    list_filter = ("rule_type", "severity", "is_active")


@admin.register(Exception)
class ExceptionAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "validation_rule",
        "severity",
        "status",
        "detected_at",
    )
    search_fields = ("employee__employee_id", "description")
    list_filter = ("severity", "status")

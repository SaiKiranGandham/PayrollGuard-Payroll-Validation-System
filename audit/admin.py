
from django.contrib import admin
from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "entity_type",
        "entity_id",
        "actor",
        "timestamp",
    )
    list_filter = ("action", "entity_type")
    search_fields = ("action", "entity_type", "entity_id", "description")
    readonly_fields = ("timestamp",)

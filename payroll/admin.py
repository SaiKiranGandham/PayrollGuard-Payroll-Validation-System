
from django.contrib import admin
from .models import (
    PayGroup,
    PayPeriod,
    TimeEntry,
    LeaveRecord,
    Allowance,
    Deduction,
    PayrollInput,
)


admin.site.register(PayGroup)
admin.site.register(PayPeriod)
admin.site.register(TimeEntry)
admin.site.register(LeaveRecord)
admin.site.register(Allowance)
admin.site.register(Deduction)
admin.site.register(PayrollInput)

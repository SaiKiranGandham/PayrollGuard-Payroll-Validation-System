
from django.shortcuts import render

from .models import Employee


def employee_list(request):
    employees = Employee.objects.all().order_by("employee_id")

    context = {
        "employees": employees,
        "total_employees": employees.count(),
        "active_employees": employees.filter(is_active=True).count(),
        "inactive_employees": employees.filter(is_active=False).count(),
    }

    return render(request, "employees/employee_list.html", context)


from django.shortcuts import render
from django.db.models import Sum, Count

from employees.models import Employee
from payroll.models import PayrollInput
from validation.models import Exception as PayrollException


def home(request):
    return render(request, "home.html")


def payroll_dashboard(request):
    total_employees = Employee.objects.filter(is_active=True).count()

    payroll_summary = PayrollInput.objects.aggregate(
        total=Sum("net_pay")
    )

    total_payroll = payroll_summary["total"] or 0

    total_payrolls = PayrollInput.objects.count()

    approved_payrolls = PayrollInput.objects.filter(
        status="APPROVED"
    ).count()

    rejected_payrolls = PayrollInput.objects.filter(
        status="REJECTED"
    ).count()

    pending_payrolls = PayrollInput.objects.filter(
        status="PENDING"
    ).count()

    draft_payrolls = PayrollInput.objects.filter(
        status="DRAFT"
    ).count()

    payroll_exceptions = PayrollException.objects.filter(
        status="OPEN"
    ).count()

    resolved_exceptions = PayrollException.objects.filter(
        status="RESOLVED"
    ).count()

    payroll_status = (
        PayrollInput.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )

    context = {
        "total_employees": total_employees,
        "total_payroll": total_payroll,
        "total_payrolls": total_payrolls,
        "approved_payrolls": approved_payrolls,
        "rejected_payrolls": rejected_payrolls,
        "pending_payrolls": pending_payrolls,
        "draft_payrolls": draft_payrolls,
        "payroll_exceptions": payroll_exceptions,
        "resolved_exceptions": resolved_exceptions,
        "payroll_status": payroll_status,
    }

    return render(request, "payroll/dashboard.html", context)


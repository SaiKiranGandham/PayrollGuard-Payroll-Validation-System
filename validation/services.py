
from decimal import Decimal

from django.db import transaction

from payroll.models import (
    TimeEntry,
    Allowance,
    Deduction,
)

from .models import ValidationRule, Exception as PayrollException


@transaction.atomic
def run_payroll_validation(payroll_input):
    employee = payroll_input.employee
    pay_period = payroll_input.pay_period

    detected = []

    def add_exception(name, description, rule_type):
        rule, _ = ValidationRule.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "rule_type": rule_type,
                "severity": "ERROR",
                "is_active": True,
            },
        )

        if not rule.is_active:
            return

        existing = PayrollException.objects.filter(
            employee=employee,
            pay_period=pay_period,
            payroll_input=payroll_input,
            validation_rule=rule,
            status="OPEN",
        ).first()

        if not existing:
            PayrollException.objects.create(
                employee=employee,
                pay_period=pay_period,
                payroll_input=payroll_input,
                validation_rule=rule,
                description=description,
                severity=rule.severity,
                status="OPEN",
            )

        detected.append(name)

    # Rule 1: Maximum working hours
    total_hours = sum(
        (
            entry.regular_hours + entry.overtime_hours
            for entry in TimeEntry.objects.filter(
                employee=employee,
                pay_period=pay_period,
            )
        ),
        Decimal("0.00"),
    )

    if total_hours > Decimal("240.00"):
        add_exception(
            "Maximum Working Hours",
            f"Total working hours are {total_hours}, exceeding 240.",
            "HOURS",
        )

    # Rule 2: Unapproved time entries
    pending_time = TimeEntry.objects.filter(
        employee=employee,
        pay_period=pay_period,
    ).exclude(approval_status="APPROVED")

    if pending_time.exists():
        add_exception(
            "Unapproved Time Entry",
            "Payroll contains time entries that are not approved.",
            "APPROVAL",
        )

    # Rule 3: Duplicate allowances
    allowance_records = Allowance.objects.filter(
        employee=employee,
        pay_period=pay_period,
    )

    duplicates = (
        allowance_records.values("allowance_type")
        .annotate(total=__import__("django.db.models", fromlist=["Count"]).Count("id"))
        .filter(total__gt=1)
    )

    if duplicates.exists():
        add_exception(
            "Duplicate Allowance",
            "Duplicate allowance records were found.",
            "DUPLICATE",
        )

    # Rule 4: Payroll total reconciliation
    expected_net = (
        payroll_input.gross_pay
        + payroll_input.total_allowances
        - payroll_input.total_deductions
    )

    if payroll_input.net_pay != expected_net:
        add_exception(
            "Payroll Reconciliation",
            f"Expected net pay {expected_net}, "
            f"but recorded net pay is {payroll_input.net_pay}.",
            "RECONCILIATION",
        )

    return detected

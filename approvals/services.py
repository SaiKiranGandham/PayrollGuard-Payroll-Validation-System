
import csv
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import Approval, ApprovalEvent, PayrollExport
from audit.models import AuditEvent
from payroll.models import PayrollInput, PayPeriod


@transaction.atomic
def process_approval(approval, action, actor=None, comments=""):
    action = action.upper()

    if action not in ["APPROVE", "REJECT"]:
        raise ValueError("Action must be APPROVE or REJECT.")

    if approval.status != "PENDING":
        raise ValueError("Only pending approvals can be processed.")

    previous_status = approval.status
    new_status = "APPROVED" if action == "APPROVE" else "REJECTED"

    approval.status = new_status
    approval.comments = comments

    if action == "APPROVE":
        approval.approved_at = timezone.now()

    approval.save()

    payroll_input = approval.payroll_input
    payroll_input.status = new_status
    payroll_input.save(update_fields=["status", "updated_at"])

    ApprovalEvent.objects.create(
        approval=approval,
        actor=actor,
        event_type=action,
        previous_status=previous_status,
        new_status=new_status,
        comments=comments,
    )

    AuditEvent.objects.create(
        actor=actor,
        action=action,
        entity_type="Approval",
        entity_id=str(approval.id),
        description=f"Payroll approval {new_status}.",
        metadata={
            "payroll_input_id": payroll_input.id,
            "previous_status": previous_status,
            "new_status": new_status,
        },
    )

    return approval


def export_approved_payroll(pay_period_id, actor=None):
    try:
        pay_period = PayPeriod.objects.get(id=pay_period_id)
    except PayPeriod.DoesNotExist:
        raise ValueError("Pay period does not exist.")

    approved_records = PayrollInput.objects.filter(
        pay_period=pay_period,
        status="APPROVED",
        approval__status="APPROVED",
    ).select_related("employee", "pay_period").distinct()

    if not approved_records.exists():
        raise ValueError("No approved payroll records available for export.")

    export_directory = Path(settings.BASE_DIR) / "exports"
    export_directory.mkdir(parents=True, exist_ok=True)

    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"payroll_period_{pay_period_id}_{timestamp}.csv"
    file_path = export_directory / file_name

    columns = [
        "employee_id",
        "employee_name",
        "pay_period_start",
        "pay_period_end",
        "basic_salary",
        "total_hours",
        "overtime_hours",
        "gross_pay",
        "total_allowances",
        "total_deductions",
        "net_pay",
        "status",
    ]

    with file_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()

        for record in approved_records:
            writer.writerow({
                "employee_id": record.employee.employee_id,
                "employee_name": (
                    f"{record.employee.first_name} "
                    f"{record.employee.last_name}"
                ),
                "pay_period_start": record.pay_period.start_date,
                "pay_period_end": record.pay_period.end_date,
                "basic_salary": record.basic_salary,
                "total_hours": record.total_hours,
                "overtime_hours": record.overtime_hours,
                "gross_pay": record.gross_pay,
                "total_allowances": record.total_allowances,
                "total_deductions": record.total_deductions,
                "net_pay": record.net_pay,
                "status": record.status,
            })

    payroll_export = PayrollExport.objects.create(
        pay_period=pay_period,
        file_name=file_name,
        export_format="CSV",
        status="COMPLETED",
        exported_at=timezone.now(),
    )

    AuditEvent.objects.create(
        actor=actor,
        action="PAYROLL_EXPORT",
        entity_type="PayrollExport",
        entity_id=str(payroll_export.id),
        description="Approved payroll records exported to CSV.",
        metadata={
            "pay_period_id": pay_period.id,
            "file_name": file_name,
            "record_count": approved_records.count(),
        },
    )

    return payroll_export, file_path

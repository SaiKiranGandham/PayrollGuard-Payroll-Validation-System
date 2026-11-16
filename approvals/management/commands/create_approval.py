from django.core.management.base import BaseCommand, CommandError

from payroll.models import PayrollInput
from employees.models import Employee
from approvals.models import Approval, ApprovalEvent


class Command(BaseCommand):
    help = "Create a payroll approval request"

    def add_arguments(self, parser):
        parser.add_argument("payroll_id", type=int)
        parser.add_argument("approver_id", type=int)

    def handle(self, *args, **options):
        payroll_id = options["payroll_id"]
        approver_id = options["approver_id"]

        try:
            payroll_input = PayrollInput.objects.get(id=payroll_id)
            approver = Employee.objects.get(id=approver_id)
        except PayrollInput.DoesNotExist:
            raise CommandError("Payroll input does not exist.")
        except Employee.DoesNotExist:
            raise CommandError("Approver employee does not exist.")

        if payroll_input.status != "DRAFT":
            raise CommandError("Only DRAFT payroll inputs can be submitted.")

        approval, created = Approval.objects.get_or_create(
            payroll_input=payroll_input,
            defaults={
                "approver": approver,
                "status": "PENDING",
            },
        )

        if not created:
            raise CommandError("An approval request already exists.")

        ApprovalEvent.objects.create(
            approval=approval,
            event_type="SUBMITTED",
            previous_status="",
            new_status="PENDING",
            comments="Payroll submitted for approval.",
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Approval request created successfully. Approval ID: {approval.id}"
            )
        )
from django.core.management.base import BaseCommand, CommandError

from approvals.models import Approval
from approvals.services import process_approval


class Command(BaseCommand):
    help = "Approve or reject a payroll approval request"

    def add_arguments(self, parser):
        parser.add_argument("approval_id", type=int)
        parser.add_argument("action", choices=["APPROVE", "REJECT"])
        parser.add_argument(
            "--comments",
            default="",
            help="Optional approval or rejection comments",
        )

    def handle(self, *args, **options):
        try:
            approval = Approval.objects.get(id=options["approval_id"])
        except Approval.DoesNotExist:
            raise CommandError("Approval request does not exist.")

        try:
            process_approval(
                approval=approval,
                action=options["action"],
                comments=options["comments"],
            )
        except ValueError as error:
            raise CommandError(str(error))

        self.stdout.write(
            self.style.SUCCESS(
                f"Approval {approval.id} successfully marked as "
                f"{approval.status}."
            )
        )
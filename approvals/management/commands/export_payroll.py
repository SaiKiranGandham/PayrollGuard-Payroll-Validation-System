from django.core.management.base import BaseCommand, CommandError

from approvals.services import export_approved_payroll


class Command(BaseCommand):
    help = "Export approved payroll records to CSV"

    def add_arguments(self, parser):
        parser.add_argument("pay_period_id", type=int)

    def handle(self, *args, **options):
        pay_period_id = options["pay_period_id"]

        try:
            payroll_export, file_path = export_approved_payroll(
                pay_period_id
            )
        except ValueError as error:
            raise CommandError(str(error))

        self.stdout.write(
            self.style.SUCCESS(
                f"Payroll export completed successfully.\n"
                f"File: {file_path}\n"
                f"Export ID: {payroll_export.id}"
            )
        )
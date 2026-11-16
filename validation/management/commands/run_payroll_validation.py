
from django.core.management.base import BaseCommand, CommandError

from payroll.models import PayrollInput
from validation.services import run_payroll_validation


class Command(BaseCommand):
    help = "Run validation for a payroll input"

    def add_arguments(self, parser):
        parser.add_argument("payroll_id", type=int)

    def handle(self, *args, **options):
        payroll_id = options["payroll_id"]

        try:
            payroll_input = PayrollInput.objects.get(id=payroll_id)
        except PayrollInput.DoesNotExist:
            raise CommandError(
                f"Payroll input with ID {payroll_id} does not exist."
            )

        results = run_payroll_validation(payroll_input)

        if results:
            self.stdout.write(
                self.style.WARNING(
                    f"Validation completed. Issues found: {len(results)}"
                )
            )
            for result in results:
                self.stdout.write(f"- {result}")
        else:
            self.stdout.write(
                self.style.SUCCESS("Validation completed. No issues found.")
            )


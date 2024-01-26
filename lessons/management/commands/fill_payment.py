from django.core.management import BaseCommand, call_command
from django.db import ProgrammingError, IntegrityError

from users.models import Payment


class Command(BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options) -> None:
        fixtures_path = 'user_payment_data.json'
        Payment.objects.all().delete()

        try:
            call_command('loaddata', fixtures_path)
        except ProgrammingError:
            pass
        except IntegrityError as e:
            self.stdout.write(f'Красный? - Invalid fixtures: {e}', self.style.NOTICE)
        else:
            self.stdout.write('Зеленый - Successfully', self.style.SUCCESS)

from django.core.management import BaseCommand

from users.models import Payment
import json


class Command(BaseCommand):
    requires_migrations_checks = True

    def handle(self, *args, **options) -> None:
        pay_data = Payment.objects.all()
        pay_list = []
        for payment in pay_data:
            pay_dict = payment.__dict__
            del pay_dict['_state']
            pay_list.append(pay_dict)

        fixtures_path = 'payment_data.json'
        print(pay_list)

        try:
            with open(fixtures_path, 'wt', encoding='utf-8') as fp:
                json.dump(pay_list, fp, ensure_ascii=True)

        except Exception as e:
            print(f'Красный? - Invalid fixtures: {e}')
        else:
            print('Зеленый - Successfully')

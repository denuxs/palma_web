import json
import os
import random
import string
from os.path import basename

import django
from django.core.files import File
from django.core.management import BaseCommand

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.pos.models import *


class Command(BaseCommand):
    help = 'It allows me to insert test data into the software'

    def load_json_from_file(self, file):
        with open(f'{settings.BASE_DIR}/deploy/json/{file}', encoding='utf-8', mode='r') as wr:
            return json.loads(wr.read())

    def handle(self, *args, **options):
        numbers = list(string.digits)

        company = Company.objects.create(
            name='LA VICTORIA',
            ruc=''.join(random.choices(numbers, k=13)),
            email='lavictoria@hotmail.com',
            phone=''.join(random.choices(numbers, k=7)),
            mobile=''.join(random.choices(numbers, k=10)),
            description='La bananera La Victoria se dedica a la producción de banano desde el año 1999',
            website='https://lavictoria.com',
            address='VQ6G+M42, Bucay, Milagro',
            tax=15.00,
        )
        image_path = f'{settings.BASE_DIR}{settings.STATIC_URL}img/default/logo.png'
        company.image.save(basename(image_path), content=File(open(image_path, 'rb')), save=False)
        company.save()

        for provider_json in self.load_json_from_file(file='provider.json'):
            Provider.objects.create(**provider_json)

        for client_json in self.load_json_from_file(file='client.json'):
            Client.objects.create(**client_json)

        for employee_json in self.load_json_from_file(file='employee.json'):
            Employee.objects.create(**employee_json)

        for activity_json in self.load_json_from_file(file='activity.json'):
            Activity.objects.create(**activity_json)

        for lot_json in self.load_json_from_file(file='lot.json'):
            Lot.objects.create(**lot_json)

        for tape_json in self.load_json_from_file(file='tape.json'):
            Tape.objects.create(**tape_json)

        for type_expense_json in self.load_json_from_file(file='type_expense.json'):
            TypeExpense.objects.create(**type_expense_json)

        for expenses_json in self.load_json_from_file(file='expenses.json'):
            expenses_json['type_expense'] = TypeExpense.objects.get_or_create(name=expenses_json.pop('type_expense'))[0]
            Expenses.objects.create(**expenses_json)

        for resource_type_json in self.load_json_from_file(file='resource_type.json'):
            ResourceType.objects.create(**resource_type_json)

        for resource_json in self.load_json_from_file(file='resource.json'):
            resource_json['resource_type'] = ResourceType.objects.get_or_create(name=resource_json.pop('resource_type'))[0]
            Resource.objects.create(**resource_json)

        for plant_type_json in self.load_json_from_file(file='plant_type.json'):
            PlantType.objects.create(**plant_type_json)

        for plant_json in self.load_json_from_file(file='plant.json'):
            plant_json['plant_type'] = PlantType.objects.get(name=plant_json.pop('plant_type'))
            plant_json['lot'] = Lot.objects.get(code=plant_json.pop('lot'))
            Plant.objects.create(**plant_json)

        for employee in Employee.objects.all():
            Contract.objects.create(employee_id=employee.id, salary=random.randint(450, 800))

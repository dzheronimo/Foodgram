import csv
import json
import os

from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Создает в БД ингредиенты по списку из файла [JSON, CSV]'

    def get_or_create_obj(self, obj_list, ext: str):
        processed_ingredients = 0
        created_ingredients = 0
        for obj in obj_list:
            if ext == 'JSON':
                ingredient, _ = Ingredient.objects.get_or_create(**obj)
            else:
                ingredient, _ = Ingredient.objects.get_or_create(
                    name=obj[0],
                    measurement_unit=obj[1]
                )
            processed_ingredients += 1
            if _:
                created_ingredients += 1

        self.stdout.write(f'Было получено {processed_ingredients} ингредиентов. \n'
                          f'Новых создано {created_ingredients} -- [{ext}]', ending='')

    def handle(self, *args, **options):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.join(parent_dir.split('backend')[0], 'data')
        filename = 'ingredients'
        json_path = os.path.join(data_folder, f'{filename}.json')
        csv_path = os.path.join(data_folder, f'{filename}.csv')
        file_exists = os.path.isfile
        if file_exists(json_path):
            with open(json_path, 'r') as file:
                object_list = json.load(file)
                self.get_or_create_obj(object_list, 'JSON')
        elif file_exists(csv_path):
            with open(csv_path, 'r', newline='') as file:
                reader = csv.reader(file, delimiter=',')
                self.get_or_create_obj(reader, 'CSV')

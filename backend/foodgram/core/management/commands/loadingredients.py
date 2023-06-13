from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Создает в БД ингредиенты по списку из файла'

    ...
# def loaddata(file_name: str):
#     path_folder = '../../data/'
#     path_file = f'{path_folder}{file_name}'
#     extension = file_name.split('.')[-1]
#
#     if extension == 'json':
#         with open(path_file, 'r') as file:
#             reader = file.read()
#             print(reader)
#     elif extension == 'csv':
#         pass

    def handle(self, *args, **options):

        self.stdout.write("Hahahah- u`r idiot", ending="")


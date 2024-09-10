import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course.settings')
application = get_wsgi_application()

import csv

from block_10.explain.task_1.models import PublicationType, BookCard, BookShelf, BookRack, Librarian, BookRoom

class Importer:
    """Класс импортера данных в БД"""

    def import_publication_type_list(self):
        """
            Возвращает список видов издания для импорта
            Авторы@Название издания@Вид издания@Год издания@Кол-во стр.@Срок окончания авторского договора@ISBN@Аннотация
        """

        types_to_save = set()
        with open('I://WORK//LEARN_CENTER//Python//python-to-middle//block_10//explain//task_1//books.csv',
                  encoding='utf-8') as f:
            rows = csv.DictReader(f, delimiter='@')

            for row in rows:
                publication_type = row['Вид издания']
                if publication_type is not None:
                    if row['Аннотация'] is None:
                        if len(row['Название издания']) != 4:  # Кривая запись
                            continue
                        publication_type = row['Название издания']

                    publication_type = publication_type.strip().lower()
                    if ('худож' in publication_type and 'лит' in publication_type):
                        publication_type = 'худож. лит-ра'
                    types_to_save.add(publication_type)

        sorted_list = list(types_to_save)
        sorted_list.sort()

        list_for_save = []
        for row in sorted_list:
            list_for_save.append(
                PublicationType(
                    name=row
                )
            )

            print(row)

        return list_for_save

    def import_books_list(self):
        """TODO"""
        """Возвращает списки для импорта
                - залов
                - стеллажей
                - полок
                - книжных карточек
            Авторы@Название издания@Вид издания@Год издания@Кол-во стр.@Срок окончания авторского договора@ISBN@Аннотация
        """

        room = []
        room_to_save = []
        rack = []
        racks_to_save = []
        shelf = []
        shelf_to_save = []
        books_to_save = []

        with open('I://WORK//LEARN_CENTER//Python//python-to-middle//block_10//explain//task_1//books.csv',
                  encoding='utf-8') as f:
            rows = csv.DictReader(f, delimiter='@')

            for row in rows:
                publication_type = row['Вид издания']
                if publication_type is not None:
                    if row['Аннотация'] is None:
                        continue
                    else:
                        if len(room_to_save) % 5 == 0:
                            room = BookRoom(
                                name=len(room_to_save) + 1,
                                librarian=Librarian.objects.first()
                            )
                            room_to_save.append(room)
                            #BookRoom.objects.create(room)

                        if len(racks_to_save) % 6 == 0:
                            rack = BookRack(
                                room=room
                            )
                            racks_to_save.append(rack)
                            #BookRack.objects.create(rack)

                        if len(shelf_to_save) % 10 == 0:
                            shelf = BookShelf(
                                name=len(shelf_to_save) + 1,
                                rack=rack
                            )
                            shelf_to_save.append(shelf)
                            #BookShelf.objects.create(shelf)

                        book_card = BookCard(
                            authors=row['Авторы'],
                            name=row['Название издания'],
                            # publication_type=row['Вид издания'],get

                            publication_number=row['Год издания'],
                            page_number=row['Кол-во стр.'],
                            publication_date=row['Срок окончания авторского договора'],
                            description=row['Аннотация'],
                            book_shelf=shelf
                        )
                        books_to_save.append(book_card)
                else:
                    # это значит аннотация в нескольких строках
                    book_card.description += " " + row['Авторы']

        return books_to_save


tt = Importer()
tt.import_books_list()

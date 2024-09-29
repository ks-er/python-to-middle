import os
from datetime import datetime, date, timedelta

from dateutil.relativedelta import relativedelta
from django.core.wsgi import get_wsgi_application
from django.db.models import Q, Count, F, Avg
from django.core.exceptions import ValidationError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course.settings')
application = get_wsgi_application()

import csv

from block_10.explain.task_1.models import PublicationType, BookCard, BookShelf, BookRack, Librarian, BookRoom, \
    BookIssueJournal, ReaderCard, Reader


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

    def import_books_list(self, save_objects = False):
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

        symbol_to_replace = "#"

        with (open('I://WORK//LEARN_CENTER//Python//python-to-middle//block_10//explain//task_1//books.csv',
                  encoding='utf-8') as f):
            rows = csv.DictReader(f, delimiter='@')

            for row in rows:
                publication_type = row['Вид издания']
                if publication_type is not None:
                    if row['Аннотация'] is None:
                        if (len(row['Вид издания']) == 4):
                            book_card.publication_type = self.get_publication_type(row['Название издания'])
                            book_card.name += row['Авторы'].replace(symbol_to_replace, "")
                            book_card.publication_number=row['Вид издания'].replace(symbol_to_replace, "")
                            book_card.page_number=self.get_page_number(row['Год издания'])
                            book_card.publication_date=self.get_publication_date(row['Кол-во стр.'])
                            book_card.ISBN=row['Срок окончания авторского договора']
                            book_card.description = row['ISBN']
                        else:
                            # Что-то совсем кривое
                            continue
                    else:
                        if len(books_to_save) % 300 == 0:
                            room = BookRoom(
                                name=len(room_to_save) + 1,
                                librarian=Librarian.objects.first()
                            )

                            room_to_save.append(room)

                        if len(books_to_save) % 60 == 0:
                            rack = BookRack(
                                name=len(racks_to_save) + 1,
                                room=room
                            )

                            racks_to_save.append(rack)

                        if len(books_to_save) % 10 == 0:
                            shelf = BookShelf(
                                name=len(shelf_to_save) + 1,
                                rack=rack
                            )

                            shelf_to_save.append(shelf)

                        book_card = BookCard(
                            authors=row['Авторы'],
                            name=row['Название издания'].replace(symbol_to_replace, ""),
                            publication_type = self.get_publication_type(row['Вид издания']),
                            publication_number=row['Год издания'],
                            page_number=self.get_page_number(row['Кол-во стр.']),
                            publication_date=self.get_publication_date(row['Срок окончания авторского договора']),
                            description=row['Аннотация'].replace(symbol_to_replace, ""),
                            isbn=row['ISBN'],
                            book_shelf=BookShelf.objects.filter(name=shelf.name).first()
                        )

                        books_to_save.append(book_card)
                else:
                    publication_name = row['Название издания']
                    if publication_name is not None:
                        if len(books_to_save) % 300 == 0:
                            room = BookRoom(
                                name=len(room_to_save) + 1,
                                librarian=Librarian.objects.first()
                            )

                            room_to_save.append(room)

                        if len(books_to_save) % 60 == 0:
                            rack = BookRack(
                                name=len(racks_to_save) + 1,
                                room=room
                            )

                            racks_to_save.append(rack)

                        if len(books_to_save) % 10 == 0:
                            shelf = BookShelf(
                                name=len(shelf_to_save) + 1,
                                rack=rack
                            )

                            shelf_to_save.append(shelf)

                        book_card = BookCard(
                            authors=row['Авторы'].replace(symbol_to_replace, ""),
                            name=publication_name.replace(symbol_to_replace, ""),
                            publication_type=PublicationType.objects.first(),
                            book_shelf=BookShelf.objects.filter(name=shelf.name).first()
                        )

                        books_to_save.append(book_card)
                    else:
                        # это значит аннотация в нескольких строках
                        if row['Авторы'] is not None:
                            if book_card.description is None:
                                book_card.description = row['Авторы'].replace(symbol_to_replace, "")
                            else:
                                book_card.description += " " + row['Авторы'].replace(symbol_to_replace, "")

        if (save_objects):
            BookRoom.objects.all().delete()
            BookRack.objects.all().delete()
            BookShelf.objects.all().delete()

            BookRoom.objects.bulk_create(room_to_save)
            BookRack.objects.bulk_create(racks_to_save)
            BookShelf.objects.bulk_create(shelf_to_save)

        return books_to_save

    def add_empty_shelfs(self):
        room_count = BookRoom.objects.count()
        rack_to_add_count = room_count * 5 - BookRack.objects.count()

        need_shelf_count = room_count * 5 * 6
        new_shelf_count = rack_to_add_count * 6
        shelf_count = BookShelf.objects.count()

        shelf_count_to_last = need_shelf_count - new_shelf_count - shelf_count

        last_rack = BookRack.objects.order_by("-id")[0]
        shelf_to_save = []
        shelf_num = 6 - shelf_count_to_last + 1
        for i in range(shelf_count_to_last):
            shelf_to_save.append(BookShelf(
                name=shelf_num+i,
                rack=last_rack
            ))

        racks_to_save = []
        last_room = last_rack.room
        rack_num = 5 - rack_to_add_count + 1
        for i in range(rack_to_add_count):
            rack = BookRack(
                name=rack_num+i,
                room=last_room
            )
            racks_to_save.append(rack)

            for shelf_number in range(6):
                shelf_to_save.append(BookShelf(
                    name=shelf_number + 1,
                    rack=rack
                ))

        BookRack.objects.bulk_create(racks_to_save)
        BookShelf.objects.bulk_create(shelf_to_save)


    def get_publication_type(self, publication_type):
        pb_type = publication_type.strip().lower()
        if ('худож' in pb_type and 'лит' in pb_type):
            pb_type = 'худож. лит-ра'

        return PublicationType.objects.filter(name__contains=pb_type).first()


    def get_publication_date(self, pb_date_str):
        if pb_date_str is None:
            return None

        pb_dat_list = pb_date_str.split('.')

        if len(pb_dat_list) != 3:
            return None
        else:
            try:
                date = datetime(int(pb_dat_list[2]), int(pb_dat_list[1]), int(pb_dat_list[0]))
            except :
                year = pb_dat_list[2]
                if len(pb_dat_list[2]) == 5:
                    year = year[:-1]
                date = datetime(int(year), int(pb_dat_list[1]), int(pb_dat_list[0])-1)
            finally:
                return date

    def get_page_number(self, page_num):
        if (page_num == 'ч. 1 - 99 ч. 2 - 144'):
            return 243
        elif (page_num == '322  328'):
            return 650
        elif (page_num == '344     360    356     242'):
            return 1302

        return page_num


class ReportHelper:

    @classmethod
    def get_book_count_by_author(cls, author):
        """Возвращает количество книг, числящихся в библиотеке по имени автора

            Args:
                author: автор книги

            Returns: количество книг в библиотеке
        """
        query = BookCard.objects.filter(authors__contains=author)
        return query.count()

    @classmethod
    def get_book_count_in_library_by_author(cls, author):
        """Возвращает количество книг в библиотеке по имени автора, имеющиеся в наличии в библиотеке

            Args:
                author: автор книги

            Returns: количество книг в наличии в библиотеке
        """
        book_id_list = list(BookIssueJournal.objects.filter(returned=False).values_list('book', flat=True))
        query = BookCard.objects.filter(authors__contains=author).filter(~Q(id__in=book_id_list))

        return query.count()

    @classmethod
    def get_popular_books_for_month(cls):
        """Возвращает количество самых популярных книг за последний месяц

            Returns: список самых популярных книг
        """
        current_date = date.today()
        start_date = current_date - relativedelta(months=1)
        q_start_date = Q(issue_journal__receipt_date__gte=start_date)
        q_end_date = Q(issue_journal__receipt_date__lte=current_date)

        query_popular_books = (BookCard.objects.annotate(
            period_book_read=Count('issue_journal', filter=q_start_date & q_end_date)
        ).filter(period_book_read__gt=0).order_by('-period_book_read'))[:10]

        result = query_popular_books.values('name', 'authors', 'period_book_read')

        return list(result)

    @classmethod
    def get_popular_moving_books_for_month(cls):
        """Возвращает количество самых перемещаемых книг за последний месяц

            Returns: список самых перемещаемых книг
        """
        current_date = date.today()
        start_date = current_date - relativedelta(months=1)
        q_start_date = Q(m_journal__move_date__gte=start_date)
        q_end_date = Q(m_journal__move_date__lte=current_date)

        query_moving_books = (BookCard.objects.annotate(
            moving_count=Count('m_journal', filter=q_start_date & q_end_date)
        ).filter(moving_count__gt=0).order_by('-moving_count'))[:10]

        result = query_moving_books.values('name', 'authors', 'moving_count')

        return list(result)

    @classmethod
    def get_active_readers(cls):
        """Возвращает 10 самых активных читателей, которые взяли больше всего книг, за прошедший месяц

            Returns: список активных читателей
        """
        current_date = date.today()
        start_date = current_date - relativedelta(months=1)
        q_start_date = Q(issue_journal__receipt_date__gte=start_date)
        q_end_date = Q(issue_journal__receipt_date__lte=current_date)

        query_popular_books = (ReaderCard.objects.annotate(
            book_count=Count('issue_journal', filter=q_start_date & q_end_date)
        ).filter(book_count__gt=0).order_by('-book_count'))[:10]

        result = query_popular_books.values('reader__last_name', 'reader__name', 'book_count')

        return list(result)

    @classmethod
    def get_overdue_returns(cls):
        """Возвращает Перечень читателей, которые просрочили возврат книг

            Returns: список читателей
        """

        current_date = date.today()
        returned_date = current_date - relativedelta(days=30)
        q_returned_date = Q(receipt_date__lte=returned_date)
        returned = Q(returned=False)

        result = (BookIssueJournal.objects.filter(returned & q_returned_date)
                  .annotate(last_name=F('reader_card__reader__last_name'), name=F('reader_card__reader__name'))
                  .order_by('last_name', 'name')
                  .values('last_name', 'name'))

        return list(result)

    @classmethod
    def get_outside_library_readers(cls):
        """Возвращает Количество книг, которые сейчас находятся на руках в разрезе читателей

            Returns: Количество книг в разрезе читателей
        """

        not_returned = Q(issue_journal__returned=False)

        outside_library_readers = (ReaderCard.objects.annotate(
            book_count=Count('issue_journal', filter=not_returned)
        ).filter(book_count__gt=0))

        result = (outside_library_readers
            .annotate(last_name=F('reader__last_name'), name=F('reader__name'))
            .values('last_name', 'name', 'book_count')
            .order_by('-book_count', 'last_name', 'name'))

        return list(result)

    @classmethod
    def get_read_pages_by_publication(cls):
        """Возвращает Среднее количество страниц в разрезе видов изданий, которые прочитали читатели за последний месяц

            Returns: список количества страниц по публикациям
        """
        current_date = date.today()
        start_date = current_date - relativedelta(months=1)
        q_start_date = Q(receipt_date__gte=start_date)
        q_end_date = Q(receipt_date__lte=current_date)

        result = (BookIssueJournal.objects.filter(q_start_date & q_end_date)
                   .annotate(publication_type=F('book__publication_type__name'))
                   .values('publication_type')
                   .annotate(avg_pages=Avg(F('book__page_number'))))

        return list(result)


reader = Reader.objects.get(id=1)
book1 = BookCard.objects.get(id=785)
book2 = BookCard.objects.get(id=578)
book3 = BookCard.objects.get(id=555)

try:
    reader.take_book(book1, True)
except ValidationError as exc:
    print(exc)

try:
    #reader.take_book(book2, True)
    reader.take_book(book3, True)
except ValidationError as exc:
    print(exc)

try:
    book465 = BookCard.objects.get(id=465)
    reader.return_book(book465)
except ValidationError as exc:
    print(exc)


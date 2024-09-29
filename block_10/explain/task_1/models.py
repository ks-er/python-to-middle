import datetime
from functools import cached_property

from django.db import (
    models,
)
from django.db.models import Q, Count
from django.core.exceptions import ValidationError


class Librarian(models.Model):
    """
    Библиотекарь
    """

    # objects = Manager
    # objects_random = RandomManager()

    last_name = models.CharField("Фамилия", max_length=30)
    name = models.CharField("Имя", max_length=30)
    fired = models.BooleanField(default=False, verbose_name="Уволен")

    class Meta:
        db_table = "librarian"
        app_label = "admin"


class PublicationType(models.Model):
    """
    Вид издания
    """

    name = models.CharField("Вид издания", max_length=50)

    class Meta:
        db_table = "publication_type"
        app_label = "admin"


class BookRoom(models.Model):
    """
    Книжный зал
    """

    name = models.IntegerField("Номер зала", default=0)
    librarian = models.ForeignKey(Librarian, on_delete=models.PROTECT)

    class Meta:
        db_table = "book_room"
        app_label = "admin"


class BookRack(models.Model):
    """
    Стеллаж
    """

    name = models.IntegerField("Номер стеллажа", default=0)
    room = models.ForeignKey(BookRoom, on_delete=models.PROTECT, related_name="racks")

    class Meta:
        db_table = "book_rack"
        app_label = "admin"
        unique_together = (("name", "room"),)


class BookShelfManager(models.Manager):

    def get_empty_shelf(self):
        shelf = (
            BookShelf.objects.annotate(book_count=Count("books"))
            .filter(book_count__lt=10)
            .first()
        )
        return shelf


class BookShelf(models.Model):
    """
    Книжная полка
    """

    bs_objects = BookShelfManager()

    name = models.IntegerField("Номер полки", default=0)
    rack = models.ForeignKey(BookRack, on_delete=models.PROTECT, related_name="shelfs")

    class Meta:
        db_table = "book_shelf"
        app_label = "admin"
        unique_together = (("name", "rack"),)


class BookCard(models.Model):
    authors = models.CharField("Автор", max_length=500)
    name = models.CharField("Название книги", max_length=500)
    publication_type = models.ForeignKey(
        PublicationType, on_delete=models.PROTECT, related_name="books"
    )
    publication_number = models.IntegerField("Номер", default=0)
    page_number = models.IntegerField("Количество страниц", default=0)
    publication_date = models.DateField("Дата издания", null=True)
    description = models.CharField("Описание", max_length=3000)
    isbn = models.CharField("ISBN", max_length=500, null=True)
    book_shelf = models.ForeignKey(
        BookShelf, on_delete=models.PROTECT, related_name="books"
    )

    class Meta:
        db_table = "book_card"
        app_label = "admin"


class MovementJournal(models.Model):
    """
    Журнал перемещения
    """

    move_date = models.DateField(
        "Дата перемещения",
        null=False,
    )
    book = models.ForeignKey(
        BookCard, on_delete=models.PROTECT, related_name="m_journal"
    )
    book_shelf_old = models.ForeignKey(
        BookShelf, on_delete=models.PROTECT, related_name="old_shelfs"
    )
    book_shelf_new = models.ForeignKey(
        BookShelf, on_delete=models.PROTECT, related_name="new_shelfs"
    )

    class Meta:
        db_table = "movement_journal"
        app_label = "admin"


class Reader(models.Model):
    """
    Читатель
    """

    last_name = models.CharField("Фамилия", max_length=30)
    name = models.CharField("Имя", max_length=30)

    @cached_property
    def reader_card(self):
        return ReaderCard.objects.get(reader=self)

    @cached_property
    def books_on_hands(self):
        return (
            BookIssueJournal.objects.filter(returned=False)
            .filter(reader_card__reader=self)
            .count()
        )

    def take_book(self, book, outside_library):
        not_returned = Q(returned=False)
        q_book = Q(book=book.pk)
        journal_records = BookIssueJournal.objects.filter(q_book & not_returned).count()

        if journal_records > 0:
            raise ValidationError("Книги нет в наличии в библиотеке.")

        if self.books_on_hands == 3:
            raise ValidationError(
                "Нельзя взять 4ую книгу для прочтения. Необходимо вернуть предыдущие книги."
            )

        BookIssueJournal.objects.create(
            receipt_date=datetime.date.today(),
            outside_library=outside_library,
            book=book,
            reader_card=self.reader_card,
        )

    def return_book(self, book):
        """
        Возвращение книги на первую свободную полку
        1. Ставится признак возврата книги в журнале выдачи книг
        2. Ставится пометка о перемещении книги на первую свободную полку
        3. Делается запись в журнале перемещения книг
        """
        not_returned = Q(returned=False)
        q_book = Q(book=book.pk)
        reader_card = Q(reader_card=self.reader_card)
        book_to_return = BookIssueJournal.objects.filter(
            q_book & not_returned & reader_card
        ).count()

        if book_to_return == 0:
            raise ValidationError("Книга уже была возвращена")

        BookIssueJournal.objects.filter(q_book & not_returned & reader_card).update(
            returned=True
        )

        old__shelf = book.book_shelf
        new_shelf = BookShelf.bs_objects.get_empty_shelf()
        BookCard.objects.filter(id=book.pk).update(book_shelf=new_shelf)

        MovementJournal.objects.create(
            move_date=datetime.date.today(),
            book=book,
            book_shelf_new=new_shelf,
            book_shelf_old=old__shelf,
        )

    class Meta:
        db_table = "reader"
        app_label = "admin"


class ReaderCard(models.Model):
    """
    Карточка читателя
    """

    receipt_date = models.DateField(
        "Дата получения",
        null=False,
    )
    reader = models.ForeignKey(Reader, on_delete=models.PROTECT)

    class Meta:
        db_table = "reader_card"
        app_label = "admin"


class BookIssueJournal(models.Model):
    """
    Журнал выдачи книг
    """

    receipt_date = models.DateField(
        "Дата выдачи",
        null=False,
    )
    book = models.ForeignKey(
        BookCard, on_delete=models.PROTECT, related_name="issue_journal"
    )
    outside_library = models.BooleanField(
        default=False, verbose_name="Чтение вне библиотеки"
    )
    returned = models.BooleanField(default=False, verbose_name="Возвращено")
    reader_card = models.ForeignKey(
        ReaderCard, on_delete=models.PROTECT, related_name="issue_journal"
    )

    class Meta:
        db_table = "book_issue_journal"
        app_label = "admin"

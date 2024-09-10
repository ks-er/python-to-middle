import uuid

from django.db import (
    models,
)

from django.db.models import Manager


class Librarian(models.Model):
    """
    Библиотекарь
    """
    #objects = Manager
    #objects_random = RandomManager()

    last_name = models.CharField('Фамилия', max_length=30)
    name = models.CharField('Имя', max_length=30)
    fired = models.BooleanField(default=False, verbose_name="Уволен")

    class Meta:
        db_table = 'librarian'
        app_label = 'admin'


class PublicationType(models.Model):
    """
    Вид издания
    """
    name = models.CharField('Вид издания', max_length=50)

    class Meta:
        db_table = 'publication_type'
        app_label = 'admin'


class BookRoom(models.Model):
    """
    Книжный зал
    """
    name = models.IntegerField('Номер зала', default=0)
    librarian = models.ForeignKey(Librarian, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_room'
        app_label = 'admin'


class BookRack(models.Model):
    """
    Стеллаж
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(BookRoom, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_rack'
        app_label = 'admin'


class BookShelf(models.Model):
    """
    Книжная полка
    """
    name = models.IntegerField('Номер полки', default=0)
    rack = models.ForeignKey(BookRack, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_shelf'
        app_label = 'admin'


class BookCard(models.Model):
    authors = models.CharField('Автор', max_length=50)
    name = models.CharField('Название книги', max_length=30)
    publication_type = models.ForeignKey(PublicationType, on_delete=models.CASCADE)
    publication_number = models.IntegerField('Номер', default=0)
    page_number = models.IntegerField('Количество страниц', default=0)
    publication_date = models.DateField('Дата издания', null=True, )
    description = models.CharField('Описание', max_length=1000)
    isbn = models.CharField('ISBN', max_length=100, null=True)
    book_shelf = models.ForeignKey(BookShelf, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_card'
        app_label = 'admin'


class MovementJournal(models.Model):
    """
    Журнал перемещения
    """
    move_date = models.DateField('Дата перемещения', null=False, )
    book = models.ForeignKey(BookCard, on_delete=models.CASCADE)
    book_shelf_old = models.ForeignKey(BookShelf, on_delete=models.CASCADE, related_name="book_shelf_old")
    book_shelf_new = models.ForeignKey(BookShelf, on_delete=models.CASCADE, related_name="book_shelf_new")

    class Meta:
        db_table = 'movement_journal'
        app_label = 'admin'


class Reader(models.Model):
    """
    Читатель
    """
    last_name = models.CharField('Фамилия', max_length=30)
    name = models.CharField('Имя', max_length=30)

    class Meta:
        db_table = 'reader'
        app_label = 'admin'


class ReaderCard(models.Model):
    """
    Карточка читателя
    """
    receipt_date = models.DateField('Дата получения', null=False, )
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reader_card'
        app_label = 'admin'

class BookIssueJournal(models.Model):
    """
    Журнал выдачи книг
    """
    receipt_date = models.DateField('Дата выдачи', null=False, )
    book = models.ForeignKey(BookCard, on_delete=models.CASCADE)
    outside_library = models.BooleanField(default=False, verbose_name="Чтение вне библиотеки")
    returned = models.BooleanField(default=False, verbose_name="Возвращено")
    reader_card = models.ForeignKey(ReaderCard, on_delete=models.CASCADE)

    class Meta:
        db_table = 'book_issue_journal'
        app_label = 'admin'







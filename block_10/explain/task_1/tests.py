from django.test import (
    TestCase,
)

from block_10.explain.task_1.implementation import Importer, ReportHelper
from block_10.explain.task_1.models import Librarian, PublicationType, BookCard


class ExplainTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Librarian.objects.all().delete()

        librarians = [
            Librarian(
                last_name='Петрова',
                name='Галина',
                fired=False),
            Librarian(
                last_name='Иванова',
                name='Светлана',
                fired=False
            ),
            Librarian(
                last_name='Сидорова',
                name='Евгения',
                fired=False
            ),
        ]

        #Librarian.objects.bulk_create(librarians)

        #PublicationType.objects.all().delete()
        im = Importer()
        #publication_types = im.import_publication_type_list()
        #PublicationType.objects.bulk_create(publication_types)

        #books = im.import_books_list(True)
        #books1 = im.import_books_list()
        #BookCard.objects.bulk_create(books1)

    def test_books_count1(self):
        self.assertEqual(ReportHelper.get_book_count_by_author('Безьев Д.А.'), 2)

    def test_books_count2(self):
        self.assertEqual(ReportHelper.get_book_count_in_library_by_author('Безьев Д.А.'), 1)

    def test_popular_books(self):
        self.assertEqual(len(ReportHelper.get_popular_books_for_month()), 3)

    def test_moving_books(self):
        self.assertEqual(len(ReportHelper.get_popular_moving_books_for_month()), 1)

    def test_active_readers(self):
        self.assertEqual(len(ReportHelper.get_active_readers()), 1)

    def test_overdue_returns(self):
        self.assertEqual(len(ReportHelper.get_overdue_returns()), 1)

    def test_outside_library_readers(self):
        self.assertEqual(len(ReportHelper.get_outside_library_readers()), 2)

    def test_read_pages_by_publication(self):
        self.assertEqual(len(ReportHelper.get_read_pages_by_publication()), 2)
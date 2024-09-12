from django.test import (
    TestCase,
)

from block_10.explain.task_1.implementation import Importer
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

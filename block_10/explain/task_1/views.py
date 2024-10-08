import datetime
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import OuterRef, F, Subquery
from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from block_10.explain.task_1.implementation import ReportHelper
from block_10.explain.task_1.models import (
    Librarian,
    PublicationType,
    BookRoom,
    BookRack,
    BookShelf,
    BookCard,
    MovementJournal,
    Reader,
    ReaderCard,
    BookIssueJournal,
)
from block_10.explain.task_1.serializers import (
    LibrarianSerializer,
    PublicationTypeSerializer,
    BookRoomSerializer,
    BookRackSerializer,
    BookShelfSerializer,
    BookCardSerializer,
    MovementJournalSerializer,
    ReaderSerializer,
    ReaderCardSerializer,
    BookIssueJournalSerializer,
)
from block_10.explain.task_1.tests import ExplainTest


class LibrarianViewSet(viewsets.ModelViewSet):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["last_name", "name"]
    ordering_fields = ["last_name", "name"]

    def perform_create(self, serializer: Serializer):
        last_name = serializer.validated_data["last_name"]
        name = serializer.validated_data["name"]

        if qs := self.queryset.filter(last_name=last_name, name=name):
            serializer.instance = qs.first()
            return
        super().perform_create(serializer)


class PublicationTypeViewSet(viewsets.ModelViewSet):
    queryset = PublicationType.objects.all()
    serializer_class = PublicationTypeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def perform_create(self, serializer: Serializer):
        name = serializer.validated_data["name"]

        if qs := self.queryset.filter(name=name):
            serializer.instance = qs.first()
            return
        super().perform_create(serializer)


class BookRoomViewSet(viewsets.ModelViewSet):
    queryset = BookRoom.objects.all()
    serializer_class = BookRoomSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        qs_room = BookRack.objects.filter(room=OuterRef("pk"))
        result = ArraySubquery(qs_room.order_by("name").values_list("name"))
        qs_result = BookRoom.objects.annotate(rack_names=result)
        return qs_result

    def perform_create(self, serializer: Serializer):
        name = serializer.validated_data["name"]

        if qs := self.queryset.filter(name=name):
            serializer.instance = qs.first()
            return
        super().perform_create(serializer)


class BookRackViewSet(viewsets.ModelViewSet):
    queryset = BookRack.objects.all()
    serializer_class = BookRackSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        qs_rack = BookShelf.bs_objects.filter(rack=OuterRef("pk"))
        result = ArraySubquery(qs_rack.order_by("name").values_list("name"))
        qs_result = BookRack.objects.annotate(shelf_names=result)
        return qs_result

    def perform_create(self, serializer: Serializer):
        name = serializer.validated_data["name"]
        room_name = serializer.validated_data["room"]["name"]

        if qs := self.queryset.filter(name=name, room__name=room_name):
            serializer.instance = qs.first()
            return
        super().perform_create(serializer)


class BookShelfViewSet(viewsets.ModelViewSet):
    queryset = BookShelf.bs_objects.all()
    serializer_class = BookShelfSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def perform_create(self, serializer: Serializer):
        name = serializer.validated_data["name"]
        rack_name = serializer.validated_data["rack"]["name"]
        room_name = serializer.validated_data["rack"]["room"]["name"]

        if qs := self.queryset.filter(
            name=name, rack__name=rack_name, rack__room__name=room_name
        ):
            serializer.instance = qs.first()
            return
        super().perform_create(serializer)


class BookCardViewSet(viewsets.ModelViewSet):
    queryset = BookCard.objects.all()
    serializer_class = BookCardSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "authors",
        "name",
        "description",
        "publication_type__name",
        "publication_date",
    ]
    ordering_fields = ["authors", "name", "publication_type__name", "publication_date"]

    def perform_create(self, serializer: Serializer):
        name = serializer.validated_data["name"]
        isbn = serializer.validated_data["isbn"]

        if qs := self.queryset.filter(name=name, isbn=isbn):
            serializer.instance = qs.first()
            return
        super().perform_create(serializer)


class MovementJournalViewSet(viewsets.ModelViewSet):
    queryset = MovementJournal.objects.all()
    serializer_class = MovementJournalSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["move_date"]
    ordering_fields = ["move_date"]

    @action(detail=False, methods=["get"], name="Move book")
    def move_book(self, request):
        data = request.GET
        book_id = data.get("book_id")
        book = BookCard.objects.get(id=book_id)
        new_shelf = BookShelf.bs_objects.get_empty_shelf()

        BookCard.objects.filter(id=book.pk).update(book_shelf=new_shelf)

        MovementJournal.objects.create(
            move_date=datetime.date.today(),
            book=book,
            book_shelf_new=new_shelf,
            book_shelf_old=book.book_shelf,
        )

        return Response({"status": status.HTTP_200_OK})


class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["last_name", "name"]
    ordering_fields = ["last_name", "name"]

    def perform_create(self, serializer: Serializer):
        last_name = serializer.validated_data["last_name"]
        name = serializer.validated_data["name"]

        if qs := self.queryset.filter(last_name=last_name, name=name):
            serializer.instance = qs.first()
            return
        super().perform_create(serializer)


class ReaderCardViewSet(viewsets.ModelViewSet):
    queryset = ReaderCard.objects.all()
    serializer_class = ReaderCardSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["receipt_date", "reader__last_name", "reader__name"]
    ordering_fields = ["receipt_date", "reader__last_name", "reader__name"]

    def perform_create(self, serializer: Serializer):
        receipt_date = serializer.validated_data["receipt_date"]
        reader_name = serializer.validated_data["reader"]["name"]
        reader_last_name = serializer.validated_data["reader"]["last_name"]

        if qs := self.queryset.filter(
            receipt_date=receipt_date,
            reader__name=reader_name,
            reader__last_name=reader_last_name,
        ):
            serializer.instance = qs.first()
            return
        super().perform_create(serializer)


class BookIssueJournalViewSet(viewsets.ModelViewSet):
    queryset = BookIssueJournal.objects.all()
    serializer_class = BookIssueJournalSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["receipt_date"]
    ordering_fields = ["receipt_date"]

    @action(detail=False, methods=["get"], name="Give to reader")
    def give_to_reader(self, request):
        data = request.GET
        book_id = data.get("book_id")
        book = BookCard.objects.get(id=book_id)
        reader_card_id = data.get("reader_card_id")
        reader_card = ReaderCard.objects.get(id=reader_card_id)
        reader_card.reader.take_book(book, True)

        return Response({"status": status.HTTP_200_OK})

    @action(detail=False, methods=["get"], name="Return to library")
    def return_to_library(self, request):
        data = request.GET
        book_id = data.get("book_id")
        book = BookCard.objects.get(id=book_id)
        reader_card_id = data.get("reader_card_id")
        reader_card = ReaderCard.objects.get(id=reader_card_id)
        reader_card.reader.return_book(book)

        return Response({"status": status.HTTP_200_OK})


def index(request):
    """Начальная загрузка данных"""
    # ExplainTest.setUpTestData()

    popular_books = ReportHelper.get_popular_books_for_month()
    moving_books = ReportHelper.get_popular_moving_books_for_month()
    active_readers = ReportHelper.get_active_readers()
    overdue_returns = ReportHelper.get_overdue_returns()
    outside_library_readers = ReportHelper.get_outside_library_readers()
    read_pages_by_publication = ReportHelper.get_read_pages_by_publication()
    rooms_info_list = ReportHelper.get_halls_list()
    unpopular_books = ReportHelper.get_unpopular_books()

    return render(
        request,
        "explain.html",
        context={
            "popular_books": popular_books,
            "moving_books": moving_books,
            "active_readers": active_readers,
            "overdue_returns": overdue_returns,
            "outside_library_readers": outside_library_readers,
            "read_pages_by_publication": read_pages_by_publication,
            "rooms_info_list": rooms_info_list,
            "unpopular_books": unpopular_books,
        },
    )

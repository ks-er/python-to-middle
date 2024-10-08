from datetime import datetime
import re

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

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


class LibrarianSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Librarian
        fields = "__all__"

    """
    def create(self, serializer: Serializer):
        a = serializer.validated_data["name"]
        b = serializer.validated_data["last_name"]
        if qs := self.queryset.filter(a=a, b=b):
            serializer.instance = qs.first()
            return
        super().create(serializer)
"""


class PublicationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PublicationType
        fields = "__all__"


class BookRoomSerializer(serializers.HyperlinkedModelSerializer):
    librarian = LibrarianSerializer()
    rack_names = serializers.CharField(max_length=100, required=False, read_only=True)

    class Meta:
        model = BookRoom
        fields = "__all__"

    def create(self, validated_data):
        librarian_data = validated_data.pop("librarian")
        name = validated_data.pop("name")
        librarian = Librarian.objects.get_or_create(**librarian_data)[0]
        room = BookRoom.objects.create(librarian=librarian, name=name)
        return room

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class LightBookRoomSerializer(BookRoomSerializer):

    class Meta:
        model = BookRoom
        fields = ["url", "name"]


class BookRackSerializer(serializers.HyperlinkedModelSerializer):
    room = LightBookRoomSerializer()
    shelf_names = serializers.CharField(max_length=100, required=False, read_only=True)

    class Meta:
        model = BookRack
        fields = ["url", "name", "room", "shelf_names"]

    def create(self, validated_data):
        room_data = validated_data.pop("room")
        librarian = Librarian.objects.all().last()
        room = BookRoom.objects.get_or_create(librarian=librarian, **room_data)[0]
        rack = BookRack.objects.create(room=room, name=validated_data["name"])
        return rack

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class BookShelfSerializer(serializers.HyperlinkedModelSerializer):
    rack = BookRackSerializer()

    class Meta:
        model = BookShelf
        fields = "__all__"

    def create(self, validated_data):
        rack_name = validated_data["rack"]["name"]
        room_name = validated_data["rack"]["room"]["name"]

        rack = BookRack.objects.filter(
            name=rack_name,
            room__name=room_name,
        )[0]

        shelf = BookShelf.bs_objects.create(rack=rack, name=validated_data["name"])

        return shelf

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class BookCardSerializer(serializers.HyperlinkedModelSerializer):
    publication_type = PublicationTypeSerializer()
    book_shelf = BookShelfSerializer()

    class Meta:
        model = BookCard
        fields = "__all__"

    def create(self, validated_data):
        pb_type_data = validated_data.pop("publication_type")
        pb_type = PublicationType.objects.get_or_create(name=pb_type_data["name"])[0]
        new_shelf = BookShelf.bs_objects.get_empty_shelf()

        book = BookCard.objects.create(
            publication_type=pb_type,
            book_shelf=new_shelf,
            authors=validated_data["authors"],
            name=validated_data["name"],
            publication_number=validated_data["publication_number"],
            page_number=validated_data["page_number"],
            publication_date=validated_data["publication_date"],
            description=validated_data["description"],
            isbn=validated_data["isbn"],
        )

        return book

    def update(self, instance, validated_data):
        instance.authors = validated_data.get("authors", instance.authors)
        instance.name = validated_data.get("name", instance.name)
        instance.publication_number = validated_data.get(
            "publication_number", instance.publication_number
        )
        instance.publication_date = validated_data.get(
            "publication_date", instance.publication_date
        )
        instance.description = validated_data.get(
            "publication_date", instance.description
        )
        instance.isbn = validated_data.get("publication_date", instance.isbn)
        instance.save()
        return instance


class MovementJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementJournal
        fields = ("book", "move_date", "book_shelf_new", "book_shelf_old")
        read_only_fields = ("book_shelf_new", "book_shelf_old")

    def create(self, validated_data):
        book = validated_data.pop("book")
        new_shelf = BookShelf.bs_objects.get_empty_shelf()

        movement_record = MovementJournal.objects.create(
            book=book,
            book_shelf_new=new_shelf,
            book_shelf_old=book.book_shelf,
            move_date=validated_data["move_date"],
        )

        return movement_record


class ReaderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reader
        fields = "__all__"


class ReaderCardSerializer(serializers.HyperlinkedModelSerializer):
    reader = ReaderSerializer()

    class Meta:
        model = ReaderCard
        fields = "__all__"

    def create(self, validated_data):
        reader_data = validated_data.pop("reader")
        receipt_date = validated_data.pop("receipt_date")
        reader = Reader.objects.get_or_create(**reader_data)[0]
        reader_card = ReaderCard.objects.create(
            reader=reader, receipt_date=receipt_date
        )
        return reader_card

    def update(self, instance, validated_data):
        instance.receipt_date = validated_data.get(
            "receipt_date", instance.receipt_date
        )
        instance.save()
        return instance


class BookIssueJournalSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookIssueJournal
        fields = (
            "book",
            "book_id",
            "receipt_date",
            "outside_library",
            "reader_card",
            "returned",
        )
        read_only_fields = ()

    def create(self, validated_data):
        print(validated_data)
        book = validated_data.pop("book")
        reader_card = validated_data.pop("reader_card")

        iss_record = BookIssueJournal.objects.create(
            receipt_date=validated_data.pop("receipt_date"),
            outside_library=validated_data.pop("outside_library"),
            book=book,
            reader_card=reader_card,
        )

        return iss_record

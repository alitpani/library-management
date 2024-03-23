# serializers.py
from os import write
from rest_framework import serializers

from .models import Books, Circulation, Members, Reservation
from rest_framework.exceptions import ValidationError as DRFValidationError


class CirculationOutputSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="book.book_name", read_only=True)
    book_copies = serializers.IntegerField(
        source="book.number_od_copies", read_only=True
    )
    member_name = serializers.CharField(source="member.member_name", read_only=True)

    class Meta:
        model = Circulation
        fields = [
            "book_copies",
            "circulation_id",
            "checkout_date",
            "return_time",
            "return_date",
            "checkout_date",
            "book_name",
            "member_name",
        ]


class CirculationSerializer(serializers.ModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Books.objects.all(), write_only=True
    )
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=Members.objects.all(), write_only=True
    )
    return_time = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = Circulation
        fields = [
            "book_id",
            "member_id",
            "return_time",
        ]

    def issue_book(self, validated_data):
        member = validated_data.pop("member_id")
        book = validated_data.pop("book_id")
        if book.number_od_copies <= 0:
            Reservation.objects.create(member=member, book=book)
            raise DRFValidationError(
                "No copies of the book available. You are added to the reservation list."
            )
        if not Circulation.can_issue_book(member, book):
            raise DRFValidationError(
                "Already an entry exists for the book and member or already an reservation exists for the book and member."
            )
        return Circulation.issue_new_book(member, book)


class ReservationOutputSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="book.book_name", read_only=True)
    member_name = serializers.CharField(source="member.member_name", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "reservation_id",
            "book_name",
            "member_name",
            "fulfillment_date",
        ]


class ReservationSerializer(serializers.ModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Books.objects.all(), write_only=True
    )
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=Members.objects.all(), write_only=True
    )

    class Meta:
        model = Reservation
        fields = [
            "book_id",
            "member_id",
        ]

    def create(self, validated_data):
        member = validated_data.pop("member_id")
        book = validated_data.pop("book_id")
        return Reservation.objects.create(member=member, book=book)

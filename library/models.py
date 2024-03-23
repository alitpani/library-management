from datetime import timedelta
from email.policy import default
from re import S
from django.db import models
from datetime import datetime

"""
- Create models for Books, Members, Circulation and Reservation. You may download the 2 datasets below
    - Circulation - to include the ‘checkout’ and ‘return’ event types
- Implement relationships and constraints that handle scenarios like multiple copies of a book, book reservations, and tracking overdue books.

"""


class Books(models.Model):
    """Books Model."""

    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=255)
    number_od_copies = models.IntegerField(default=0)

    def reduce_copies(self):
        """Reduce Copies.
        Reduce the number of copies by 1.
        """
        self.number_od_copies -= 1
        self.save()

    def add_copies(self):
        """Add Copies.
        Add the number of copies by 1.
        """
        self.number_od_copies += 1
        self.save()


class Members(models.Model):
    """Members Model."""

    member_id = models.AutoField(primary_key=True)
    member_name = models.CharField(max_length=255)


class Circulation(models.Model):
    """Circulation Model."""

    circulation_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(
        Members, on_delete=models.CASCADE, related_name="circulations"
    )
    book = models.ForeignKey(
        Books, on_delete=models.CASCADE, related_name="circulations"
    )
    checkout_date = models.DateTimeField(null=True, blank=True)
    return_time = models.IntegerField(default=30)
    return_date = models.DateTimeField(null=True, blank=True)

    @classmethod
    def can_issue_book(cls, member, book):
        """Can Issue Book.
        Check if a book can be issued.
        if already an entry exists for the book and member, return False.
        Or already an reservation exists for the book and member, return False.
        """
        if cls.objects.filter(
            member=member, book=book, return_date__isnull=True
        ).exists():
            return False
        elif Reservation.objects.filter(
            member=member, book=book, fulfillment_date__isnull=True
        ).exists():
            return False
        return True

    @classmethod
    def issue_new_book(cls, member, book, return_time=None):
        """Issue Book to Member.
        Issue an book and if the book is available, reduce the number of copies by 1 and set the return date to 30 days after the checkout date.
        If the book is not availabe make a reservation.
        """
        book.reduce_copies()
        book.save()
        circulation = cls(member=member, book=book, checkout_date=datetime.now())
        if return_time:
            circulation.return_time = return_time
        circulation.save()
        return circulation

    def issue_reserved_book(self, member, book):
        """Issue Reserved Book.
        Issue a reserved book to a member and set the return date to 30 days after the checkout date.
        """
        self.member = member
        self.book = book
        book.reduce_copies()
        self.checkout_date = datetime.now()
        self.return_date = self.checkout_date + timedelta(days=30)
        self.save()
        return self

    def return_book(self):
        """Return Book.
        Return a book and increase the number of copies by 1.
        """
        self.book.add_copies()
        self.return_date = datetime.now()
        self.save()
        reservations = Reservation.objects.filter(
            member=self.member, book=self.book, fulfillment_date__isnull=True
        ).all()
        for reservation in reservations:
            if self.can_issue_book(reservation.member, reservation.book):
                self.issue_reserved_book(reservation.member, reservation.book)
                reservation.fulfillment_date = datetime.now()
                reservation.save()
        return self


# - Reservation - to ‘reserve’ a book when no copies are available to check out and ‘fulfill’ when the copy becomes available (i.e., after it is returned)
class Reservation(models.Model):
    """Reservation Model."""

    reservation_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(
        Members, on_delete=models.CASCADE, related_name="reservations"
    )
    book = models.ForeignKey(
        Books, on_delete=models.CASCADE, related_name="reservations"
    )
    reservation_date = models.DateTimeField(default=datetime.now())
    fulfillment_date = models.DateTimeField(null=True, blank=True)

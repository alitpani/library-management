from rest_framework.decorators import action
from rest_framework.response import Response as DRFResponse
from rest_framework import status

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import *
from .serializers import *


class CirculationViewSet(viewsets.ModelViewSet):
    queryset = Circulation.objects.all()
    serializer_class = CirculationOutputSerializer

    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request, pk=None):
        """Checkout a book."""
        serializer = CirculationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        circulation = serializer.issue_book(serializer.validated_data)
        output_serializer = CirculationOutputSerializer(circulation)
        return DRFResponse(output_serializer.data)

    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        """Return a book."""
        circulation = self.get_object()
        if not circulation.return_date:
            return DRFResponse(
                {"message": "Book already returned"}, status=status.HTTP_400_BAD_REQUEST
            )
        circulation.return_book()
        return DRFResponse(
            {"message": "Book returned successfully"}, status=status.HTTP_200_OK
        )


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

class ListingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing listing instances.
    """
    queryset = Listing.objects.all().order_by('-created_at')
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing booking instances.
    """
    queryset = Booking.objects.all().order_by('-booked_at')
    serializer_class = BookingSerializer

from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
"""
    A viewset for handling payments via Chapa.
    """
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Booking, Payment
import requests
import uuid
import os

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
class PaymentViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def create(self, request):
        booking_id = request.data.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)

        tx_ref = str(uuid.uuid4())
        amount = float(booking.total_price)

        secret_key = os.getenv('CHAPA_SECRET_KEY')

        payload = {
            'amount': amount,
            'currency': 'ETB',
            'email': booking.user_email,
            'first_name': booking.user_name,
            'last_name': 'Customer',
            'tx_ref': tx_ref,
            'callback_url': 'https://yourdomain.com/api/payments/verify/',
        }

        headers = {
            'Authorization': f'Bearer {secret_key}',
            'Content-Type': 'application/json',
        }

        url = 'https://api.chapa.co/v1/transaction/initialize'
        response = requests.post(url, json=payload, headers=headers)
        chapa_response = response.json()

        Payment.objects.create(
            booking=booking,
            amount=amount,
            email=booking.user_email,
            first_name=booking.user_name,
            last_name='Customer',
            tx_ref=tx_ref,
            status='Pending',
        )

        return Response(chapa_response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def verify(self, request):
        tx_ref = request.query_params.get('tx_ref')
        payment = get_object_or_404(Payment, tx_ref=tx_ref)

        secret_key = os.getenv('CHAPA_SECRET_KEY')
        url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
        headers = {'Authorization': f'Bearer {secret_key}'}

        response = requests.get(url, headers=headers)
        chapa_data = response.json()
        status_value = chapa_data.get('data', {}).get('status')

        if status_value == 'success':
            payment.status = 'Completed'
            payment.chapa_transaction_id = chapa_data.get('data').get('id')
            payment.save()

            booking = payment.booking
            booking.status = 'Paid'
            booking.save()

        else:
            payment.status = 'Failed'
            payment.save()

        return Response(chapa_data)

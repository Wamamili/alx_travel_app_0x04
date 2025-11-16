from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
"""
    A viewset for handling payments via Chapa.
    """
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
import uuid
import os

from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_confirmation_email


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for Listing objects."""
    queryset = Listing.objects.all().order_by('-created_at')
    serializer_class = ListingSerializer


class PaymentViewSet(viewsets.ViewSet):
    """Simple payment endpoints to initialize and verify Chapa transactions.

    - `POST /payments/initialize/` with `booking_id` to create a transaction.
    - `GET  /payments/verify/?tx_ref=...` to verify a transaction.
    Note: Booking model does not include a `status` field, so only Payment
    records are updated here.
    """

    @action(detail=False, methods=["post"], url_path="initialize")
    def initialize(self, request):
        booking_id = request.data.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)

        tx_ref = str(uuid.uuid4())
        amount = float(booking.total_price)

        secret_key = os.getenv('CHAPA_SECRET_KEY')

        payload = {
            'amount': amount,
            'currency': 'ETB',
            'email': booking.customer_email,
            'first_name': booking.customer_name,
            'last_name': 'Customer',
            'tx_ref': tx_ref,
            'callback_url': 'https://yourdomain.com/api/payments/verify/',
        }

        headers = {
            'Authorization': f'Bearer {secret_key}',
            'Content-Type': 'application/json',
        }

        url = 'https://api.chapa.co/v1/transaction/initialize'
        resp = requests.post(url, json=payload, headers=headers)
        chapa_response = resp.json()

        Payment.objects.create(
            booking=booking,
            amount=amount,
            email=booking.customer_email,
            first_name=booking.customer_name,
            last_name='Customer',
            tx_ref=tx_ref,
            status='Pending',
        )

        return Response(chapa_response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="verify")
    def verify(self, request):
        tx_ref = request.query_params.get('tx_ref')
        payment = get_object_or_404(Payment, tx_ref=tx_ref)

        secret_key = os.getenv('CHAPA_SECRET_KEY')
        url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
        headers = {'Authorization': f'Bearer {secret_key}'}

        resp = requests.get(url, headers=headers)
        chapa_data = resp.json()
        status_value = chapa_data.get('data', {}).get('status')

        if status_value == 'success':
            payment.status = 'Completed'
            payment.chapa_transaction_id = chapa_data.get('data', {}).get('id')
            payment.save()
        else:
            payment.status = 'Failed'
            payment.save()

        return Response(chapa_data)


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for Booking objects with background email on create."""
    queryset = Booking.objects.all().order_by('-booked_at')
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # Trigger background email task (Celery)
        try:
            send_booking_confirmation_email.delay(
                booking.id,
                booking.customer_email,
                booking.customer_name,
                booking.listing.title,
                booking.check_in.strftime("%Y-%m-%d"),
                booking.check_out.strftime("%Y-%m-%d"),
            )
        except Exception:
            # If the task system is not configured, don't break the request.
            pass

        return Response(serializer.data, status=status.HTTP_201_CREATED)

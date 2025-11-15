from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(booking_id, customer_email, customer_name, listing_title, check_in, check_out):
    subject = f"Booking Confirmation for {listing_title}"
    message = (
        f"Hello {customer_name},\n\n"
        f"Your booking for {listing_title} from {check_in} to {check_out} has been confirmed.\n\n"
        f"Thank you for booking with us!"
    )
    from_email = "no-reply@alxtravelapp.com"
    send_mail(subject, message, from_email, [customer_email])
    return True

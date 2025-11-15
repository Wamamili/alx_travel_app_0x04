from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Booking
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_booking_confirmation_email(self, booking_id, customer_email, customer_name, listing_title, check_in, check_out):
    """Send booking confirmation email with retry logic."""
    try:
        subject = f"Booking Confirmation for {listing_title}"
        message = (
            f"Hello {customer_name},\n\n"
            f"Your booking for {listing_title} from {check_in} to {check_out} has been confirmed.\n\n"
            f"Thank you for booking with us!"
        )
        from_email = "no-reply@alxtravelapp.com"
        
        result = send_mail(subject, message, from_email, [customer_email])
        logger.info(f"Booking confirmation email sent for booking {booking_id}")
        return {'status': 'success', 'booking_id': booking_id, 'email_sent': result}
    
    except Exception as exc:
        logger.error(f"Error sending booking confirmation email: {exc}")
        # Retry with exponential backoff: 60s, 120s, 240s
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 60)


@shared_task
def cleanup_old_bookings():
    """Remove bookings older than 1 year."""
    try:
        one_year_ago = timezone.now() - timedelta(days=365)
        old_bookings = Booking.objects.filter(booked_at__lt=one_year_ago)
        count = old_bookings.count()
        
        # Archive instead of delete (if you have an archive model)
        # For now, just log them
        logger.info(f"Found {count} bookings older than 1 year")
        
        # old_bookings.delete()  # Uncomment if you want to delete
        return {'status': 'success', 'bookings_cleaned': count}
    
    except Exception as exc:
        logger.error(f"Error cleaning up old bookings: {exc}")
        return {'status': 'error', 'error': str(exc)}


@shared_task
def send_booking_reminders():
    """Send reminders to customers 24 hours before check-in."""
    try:
        tomorrow = timezone.now() + timedelta(days=1)
        upcoming_bookings = Booking.objects.filter(check_in__date=tomorrow.date())
        
        count = 0
        for booking in upcoming_bookings:
            subject = f"Reminder: Your booking for {booking.listing.title} is tomorrow!"
            message = (
                f"Hello {booking.customer_name},\n\n"
                f"This is a reminder that your booking for {booking.listing.title} "
                f"starts tomorrow ({booking.check_in.date()}).\n\n"
                f"Check-in time: 3:00 PM\n"
                f"Please ensure you have all necessary documents ready.\n\n"
                f"Thank you!"
            )
            from_email = "no-reply@alxtravelapp.com"
            
            try:
                send_mail(subject, message, from_email, [booking.customer_email])
                count += 1
            except Exception as e:
                logger.error(f"Failed to send reminder for booking {booking.id}: {e}")
        
        logger.info(f"Sent {count} booking reminders")
        return {'status': 'success', 'reminders_sent': count}
    
    except Exception as exc:
        logger.error(f"Error sending booking reminders: {exc}")
        return {'status': 'error', 'error': str(exc)}


@shared_task(bind=True, max_retries=2)
def process_payment_callback(self, payment_id, chapa_status):
    """Process payment callback from Chapa."""
    try:
        from .models import Payment
        payment = Payment.objects.get(id=payment_id)
        
        if chapa_status == 'success':
            payment.status = 'Completed'
            message = f"Payment {payment.tx_ref} completed successfully"
        else:
            payment.status = 'Failed'
            message = f"Payment {payment.tx_ref} failed"
        
        payment.save()
        logger.info(message)
        return {'status': 'success', 'message': message}
    
    except Exception as exc:
        logger.error(f"Error processing payment callback: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def debug_task():
    """Debug task for testing Celery setup."""
    logger.info("Debug task executed successfully")
    return {'status': 'success', 'message': 'Debug task ran'}

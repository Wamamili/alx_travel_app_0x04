README.md
Listings Service

This Django app handles property listings, bookings, reviews, and payments for the travel platform.

The app is structured to support clean API development, automated documentation, relational data modeling, and extendable features across milestones.

Features
1. Listings

• Add, view, update, and delete travel listings
• Store title, description, location, nightly price, and availability
• Automatic timestamps for auditing and analytics

2. Bookings

• Customers can book listings
• Stores check-in, check-out, and computed total price
• Linked directly to a listing
• Tracks precise booking timestamp

3. Reviews

• Users leave reviews for listings
• Ratings validated with a database constraint
• Supports optional comment field

4. Payments

• Handles booking payments
• Tracks amount, method, status, and timestamp
• Enforces unique booking-payment relationship
• Supports PENDING, COMPLETED, and FAILED states

Project Structure
listings/
  ├── migrations/
  ├── models.py
  ├── views.py
  ├── serializers.py
  ├── urls.py
  ├── tests.py

API Endpoints
Listings

GET /listings/
GET /listings/<id>/
POST /listings/
PUT /listings/<id>/
DELETE /listings/<id>/

Bookings

GET /bookings/
POST /bookings/
GET /bookings/<id>/

Reviews

POST /reviews/
GET /listings/<id>/reviews/

Payments

POST /payments/
GET /payments/<id>/

Models Overview
Listing

Stores details about a travel property including price and availability.

Booking

Connected to a listing and includes customer details and dates.

Review

Linked to a listing with a rating range of 1 to 5, enforced by a database constraint.

Payment

Linked to a booking. One booking has one payment. Tracks status, method, and amount.

Requirements

• Python 3.10 or higher
• Django 4+
• djangorestframework
• drf-yasg or drf-spectacular for documentation

Install dependencies:

pip install -r requirements.txt

Running the Project

Apply migrations:

python manage.py migrate


Start server:

python manage.py runserver

API Documentation

Swagger UI is available at:

/swagger/


Redoc:

/redoc/


Ensure you added API docs in your main urls.py:

path('swagger/', schema_view.with_ui('swagger')),

Milestone Summary
Milestone 1

Project setup, database configuration, initial Listing model.

Milestone 2

Added Booking and Review models, API routes, and validation.

Milestone 3

Integrated Payment model
Linked payments to bookings
Enforced unique constraints
Added payment-related API endpoints





alx_travel_app

Project Overview
alx_travel_app is a Django REST Framework project for managing listings, bookings, customer reviews, payments, and automated email confirmations. The application mirrors the workflow of real travel and accommodation platforms by integrating payments, background tasks, and API documentation.

Technologies
Django
Django REST Framework
PostgreSQL
Chapa Payments API
Celery
RabbitMQ
SMTP Email Backend
drf-spectacular for API documentation

Project Structure
alx_travel_app
listings
models.py
views.py
urls.py
serializers.py
tasks.py
alx_travel_app
settings.py
celery.py
README.md

Milestone Summary

Milestone 1
Project setup, database configuration, initial Listing model.

Milestone 2
Added Booking and Review models, API routes, and validation.

Milestone 3
Integrated Payment model
Linked payments to bookings
Enforced unique constraints
Added payment-related API endpoints

Milestone 4
Integrated Chapa API for payment initiation and verification.
Added payment workflow including pending, completed, and failed statuses.
Linked transactions to bookings.
Tested sandbox payment flows.

Milestone 5
Added Celery and RabbitMQ for background task processing.
Implemented asynchronous booking confirmation emails.
Updated BookingViewSet to trigger email tasks on creation.
Verified email sending using Celery workers and SMTP backend.

Models Overview

Listing
title
description
location
price_per_night
available
created_at
updated_at

Booking
listing (ForeignKey)
customer_name
customer_email
check_in
check_out
total_price
booked_at

Review
listing (ForeignKey)
reviewer_name
rating
comment
created_at

Payment
booking (OneToOneField)
amount
transaction_id
status (Pending, Completed, Failed)
created_at

Payment Workflow Summary

User creates a booking.

System initiates payment by contacting Chapa API.

Transaction ID is stored with status Pending.

User completes payment through Chapa’s checkout link.

System verifies payment via Chapa verification endpoint.

Status is updated to Completed or Failed.

On success, a Celery task sends a confirmation email.

API Documentation (Swagger and Redoc)

API documentation is automatically generated using drf-spectacular.

Setup in settings.py
SPECTACULAR_SETTINGS = {
'TITLE': 'ALX Travel App API',
'DESCRIPTION': 'API documentation for listings, bookings, reviews, and payments.',
'VERSION': '1.0.0'
}

Routes in project urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
path('api/redoc/', SpectacularRedocView.as_view(url_name='schema')),
]

Swagger URL
/api/docs/

Redoc URL
/api/redoc/

Celery Background Task Setup

Celery Configuration (celery.py)
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
app = Celery('alx_travel_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

Celery Worker Command
celery -A alx_travel_app worker --loglevel=info

RabbitMQ Start Command
sudo systemctl start rabbitmq-server

Email Task (listings/tasks.py)
A shared task sends booking confirmation emails asynchronously.

Trigger Point
BookingViewSet calls send_booking_confirmation_email.delay() after creating a booking.

Running the Project

Install dependencies
pip install -r requirements.txt

Start RabbitMQ
sudo systemctl start rabbitmq-server

Run Celery worker
celery -A alx_travel_app worker --loglevel=info

Run Django server
python manage.py runserver

Testing

Use Postman or Thunder Client to test all endpoints:
GET, POST, PUT, DELETE for:
Listings
Bookings
Reviews
Payments initiation
Payment verification

Test Swagger documentation at:
http://127.0.0.1:8000/api/docs/

Endpoints Overview

Listings
GET /api/listings/
POST /api/listings/
GET /api/listings/<id>/
PUT /api/listings/<id>/
DELETE /api/listings/<id>/

Bookings
GET /api/bookings/
POST /api/bookings/
PUT /api/bookings/<id>/
DELETE /api/bookings/<id>/

Payments
POST /api/payments/initiate/
GET /api/payments/verify/<transaction_id>/

Reviews
GET /api/reviews/
POST /api/reviews/

Next Steps
Add email templates for HTML-based booking confirmations.
Add webhook support for Chapa payment callbacks.
Implement rate limiting and throttling for API protection.
Deploy using Render or PythonAnywhere with worker processes.
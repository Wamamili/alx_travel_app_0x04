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
# ALX Travel App

API service for managing travel property listings, bookings, reviews and payments.

This repository contains a Django REST Framework application that models a simple travel marketplace and includes:
- Listings (properties)
- Bookings (reservations)
- Reviews
- Payments (Chapa integration)
- Background tasks (Celery + RabbitMQ)

---

**Features**

- **Listings**: CRUD endpoints for properties with price and availability.
- **Bookings**: Create bookings tied to listings; calculates total price.
- **Reviews**: Ratings (1-5) and comments validated at the DB level.
- **Payments**: Payment initiation and verification via Chapa; `Payment` model tracks status.
- **Background Tasks**: Asynchronous emails and periodic jobs using Celery + RabbitMQ.
- **Auto API Docs**: Swagger/OpenAPI UI exposed for easy exploration.

---

**Quick Start (Local development)**

- **Requirements**: `Python 3.10+`
- Install dependencies:

```bash
pip install -r requirements.txt
```

- Copy the example environment file and update values:

```bash
cp .env.example .env
# edit .env and fill in SECRET_KEY, DB credentials, etc.
```

- Apply migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

- Run the development server:

```bash
python manage.py runserver
```

- Visit the API docs:

```
http://127.0.0.1:8000/swagger/
```

---

**Project Structure (high level)**

- `alx_travel_app/` — Project settings and WSGI/Celery configuration
- `listings/` — App: models, views, serializers, urls, tasks, management commands
- `requirements.txt` — Pinned dependencies
- `Procfile`, `runtime.txt` — Deployment helpers
- `README.md` — This file

---

**Environment Variables (.env)**

- `SECRET_KEY` — Django secret key
- `DEBUG` — `True`/`False`
- `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — DB config
- `ALLOWED_HOSTS` — comma-separated host list
- `EMAIL_*` — SMTP configuration
- `CELERY_BROKER_URL` — e.g. `amqp://user:pass@rabbit-host:5672//`
- `CELERY_RESULT_BACKEND` — e.g. `redis://localhost:6379/0`
- `CHAPA_SECRET_KEY` — payment provider secret

Refer to `.env.example` for full list.

---

**Celery & Background Tasks**

- Start a Celery worker locally:

```bash
celery -A alx_travel_app worker -l info
```

- Start Celery Beat (periodic tasks):

```bash
celery -A alx_travel_app beat -l info
```

- Useful tasks are defined in `listings/tasks.py` (`send_booking_confirmation_email`, `send_booking_reminders`, `cleanup_old_bookings`).

Note: On PythonAnywhere you must use a paid account to enable RabbitMQ and long-running background workers.

---

**API Endpoints (examples)**

- Listings
  - `GET /api/listings/`
  - `POST /api/listings/`
  - `GET /api/listings/{id}/`
  - `PUT /api/listings/{id}/`
  - `DELETE /api/listings/{id}/`

- Bookings
  - `GET /api/bookings/`
  - `POST /api/bookings/`
  - `GET /api/bookings/{id}/`

- Payments
  - `POST /api/payments/initialize/`
  - `GET  /api/payments/verify/?tx_ref=...`

- Reviews
  - `GET /api/listings/{id}/reviews/`
  - `POST /api/reviews/`

---

**Deployment (PythonAnywhere)**

1. Create a paid PythonAnywhere account (RabbitMQ & background workers require paid plan).
2. Clone repo to your PythonAnywhere home directory.
3. Create a virtualenv and install `requirements.txt`.
4. Configure `.env` with DB and RabbitMQ credentials.
5. Run migrations and `collectstatic`.
6. Configure WSGI using `wsgi_pythonanywhere.py` (update path and username).
7. Add background tasks in the PythonAnywhere **Tasks** tab to run Celery worker and Beat.

See `PYTHONANYWHERE_DEPLOYMENT.md` and `CELERY_RABBITMQ_SETUP.md` for step-by-step instructions and troubleshooting.

---

**Testing & CI**

- Use the provided management command `test_celery` to validate Celery tasks (if worker is running).
- Run unit tests with:

```bash
python manage.py test
```

---

**Contributing**

- Fork the repository and open PRs against `main`.
- Follow the existing code style and add tests for new features.

---

**License**

This project is provided as-is for learning and demonstration purposes. Add an appropriate license if you plan to publish or share the code publicly.

---

If you'd like, I can also:

- Add badges (build / coverage)
- Wire up a GitHub Actions workflow for tests and lint
- Add HTML email templates and webhook handlers for Chapa


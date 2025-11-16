from django.core.management.base import BaseCommand
from listings.models import Listing, Booking, Review
from django.utils import timezone
import random
from datetime import timedelta, date

class Command(BaseCommand):
    help = "Seed the database with sample listings, bookings, and reviews."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding data..."))

        # Clear existing data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()

        # Create sample listings
        listings_data = [
            {"title": "Beachfront Paradise", "description": "A stunning beachside villa.", "location": "Mombasa", "price_per_night": 120.00},
            {"title": "Mountain Retreat", "description": "Peaceful cabin in the hills.", "location": "Nanyuki", "price_per_night": 90.00},
            {"title": "City Lights Apartment", "description": "Modern apartment in Nairobi CBD.", "location": "Nairobi", "price_per_night": 75.00},
        ]

        listings = []
        for data in listings_data:
            listing = Listing.objects.create(**data)
            listings.append(listing)

        # Generate sample bookings & reviews
        for listing in listings:
            for i in range(2):
                check_in = date.today() + timedelta(days=random.randint(1, 10))
                check_out = check_in + timedelta(days=random.randint(2, 5))
                total_price = (check_out - check_in).days * float(listing.price_per_night)
                Booking.objects.create(
                    listing=listing,
                    customer_name=f"Customer {i+1}",
                    customer_email=f"customer{i+1}@example.com",
                    check_in=check_in,
                    check_out=check_out,
                    total_price=total_price
                )

            for j in range(3):
                Review.objects.create(
                    listing=listing,
                    reviewer_name=f"Reviewer {j+1}",
                    rating=random.randint(3, 5),
                    comment=f"This is review {j+1} for {listing.title}."
                )

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))

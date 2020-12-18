from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):

    help = "Create fake amenities"

    # def add_arguments(self, parser):
    #     parser.add_argument("--times", help="how many times do you want?")

    def handle(self, *args, **options):
        amenities = [
            "Kitchen",
            "Shampoo",
            "Heating",
            "Air conditioning",
            "Washer",
            "Dryer",
            "Wifi",
            "Breakfast",
            "Indoor fireplace",
            "Hangers",
            "Iron",
            "Hair dryer",
            "Dedicated workspace",
            "TV",
            "High chair",
            "Self check-in",
            "Smoke alarm",
            "Carbon monoxide alarm",
            "Private bathroom",
            "Piano",
            "Beachfront",
            "Waterfront",
        ]
        for a in amenities:
            Amenity.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS(f"{len(amenities)} Amenities Created"))

from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):

    help = "Create fake facilities"

    # def add_arguments(self, parser):
    #     parser.add_argument("--times", help="how many times do you want?")

    def handle(self, *args, **options):
        facilities = [
            "Free parking on premises",
            "Gym",
            "Hot tub",
            "Pool",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} Facility Created"))

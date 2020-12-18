import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    help = "Create fake reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="how many reviews do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "Accuracy": lambda x: random.randint(0, 6),
                "Communication": lambda x: random.randint(0, 6),
                "Cleanliness": lambda x: random.randint(0, 6),
                "Location": lambda x: random.randint(0, 6),
                "Check_in": lambda x: random.randint(0, 6),
                "Value": lambda x: random.randint(0, 6),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Reviews Created"))

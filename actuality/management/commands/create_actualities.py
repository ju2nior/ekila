import os
import random
import tempfile
from datetime import timedelta

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from PIL import Image
from PIL import ImageDraw

from actuality.models import Actuality


class Command(BaseCommand):
    help = "Creates 10 random actualities with specified category"

    def add_arguments(self, parser):
        parser.add_argument(
            "category",
            type=str,
            help="Category for the actualities (Afrique, Europe, Social, Reste du monde)",
        )

    def handle(self, *args, **options):
        category = options["category"]
        titles = [
            "Nouvelle politique économique",
            "Développements technologiques récents",
            "Événement culturel majeur",
            "Progrès dans la recherche médicale",
            "Changements climatiques importants",
            "Compétition sportive internationale",
            "Innovations dans l'éducation",
            "Découverte scientifique",
            "Tendances économiques mondiales",
            "Réforme sociale",
        ]

        texts = [
            "Une analyse approfondie des récents développements dans ce domaine.",
            "Les experts partagent leurs perspectives sur cette question importante.",
            "Comment cette évolution impacte-t-elle notre quotidien?",
            "Les implications à long terme de ces changements.",
            "Une interview exclusive avec les principaux acteurs de ce secteur.",
            "Les défis et opportunités présentés par cette situation.",
            "Un regard sur les données statistiques récentes.",
            "Les réactions du public face à ces annonces.",
            "Comparaison avec les tendances historiques.",
            "Prévisions pour les mois à venir.",
        ]

        usernames = ["admin", "editor1", "reporter2", "journalist3", "guest_writer"]

        for i in range(10):
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                img = Image.new(
                    "RGB",
                    (800, 600),
                    color=(
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    ),
                )
                draw = ImageDraw.Draw(img)
                draw.text(
                    (100, 300), f"Image {i+1} for {category}", fill=(255, 255, 255)
                )
                img.save(temp_file.name, "PNG")

                actuality = Actuality(
                    category=category,
                    title=f"{random.choice(titles)} {i+1}",
                    text=random.choice(texts),
                    is_up_to_date=random.choice([True, False]),
                    video_link="https://www.youtube.com/watch?v=DCK_IohKSik",
                    username=random.choice(usernames),
                    created_at=timezone.now() - timedelta(days=random.randint(0, 30)),
                )

                with open(temp_file.name, "rb") as img_file:
                    actuality.image.save(
                        f"{category}-{i+1}.png", File(img_file), save=False
                    )

                actuality.save()
                os.unlink(temp_file.name)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created actuality: {actuality.title}")
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created 10 actualities for category: {category}"
            )
        )

from django.core.management.base import BaseCommand
from django.utils import timezone

from tarif.models import AdPlacement
from tarif.models import AdvertisingOffer
from tarif.models import OfferCategory
from tarif.models import OfferOption


class Command(BaseCommand):
    help = (
        "Seed initial data for tarif module (categories, offers, options, placements)"
    )

    def handle(self, *args, **kwargs):
        categories = [
            {"name": "Audio", "description": "Spots publicitaires audio de 20s à 40s"},
            {
                "name": "Site Web",
                "description": "Bannières et carrousels sur notre plateforme web",
            },
            {"name": "Application PWA", "description": "Affichage dans l'application"},
            {
                "name": "Popup",
                "description": "Fenêtres popup sur les pages les plus visitées",
            },
        ]

        categorie_instances = []
        for cat in categories:
            obj, created = OfferCategory.objects.get_or_create(**cat)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Catégorie {obj.name} {'créée' if created else 'existante'}"
                )
            )
            categorie_instances.append(obj)

        offres = [
            {
                "name": "Spot Radio 20s",
                "description": "Diffusion de spot de 20 secondes.",
                "support_type": "audio",
                "category": categorie_instances[0],
                "unit_price": 19995,
                "audio_durations": "20s",
            },
            {
                "name": "Spot Radio 30s",
                "description": "Diffusion de spot de 30 secondes.",
                "support_type": "audio",
                "category": categorie_instances[0],
                "unit_price": 29995,
                "audio_durations": "30s",
            },
            {
                "name": "Spot Radio 40s",
                "description": "Diffusion de spot de 40 secondes.",
                "support_type": "audio",
                "category": categorie_instances[0],
                "unit_price": 39995,
                "audio_durations": "40s",
            },
            {
                "name": "Carrousel haut de Page",
                "description": "Bannière page d’accueil.",
                "support_type": "site",
                "category": categorie_instances[1],
                "unit_price": 59995,
            },
            {
                "name": "Carrousel Bas de Page",
                "description": "Affichage en carrousel en bas des pages.",
                "support_type": "site",
                "category": categorie_instances[1],
                "unit_price": 59995,
            },
            {
                "name": "Bannière Article",
                "description": "Bannière entre les articles.",
                "support_type": "site",
                "category": categorie_instances[1],
                "unit_price": 8000,
            },
            {
                "name": "Popup",
                "description": "Popup sortant toutes les 10 chansons",
                "support_type": "mobile",
                "category": categorie_instances[2],
                "unit_price": 9995,
            },
            {
                "name": "Pochette audio",
                "description": "Carrousel d’annonces dans l’app.",
                "support_type": "mobile",
                "category": categorie_instances[2],
                "unit_price": 24995,
            },
        ]

        offre_instances = []
        for offre in offres:
            obj, created = AdvertisingOffer.objects.get_or_create(
                name=offre["name"],
                defaults={
                    "description": offre.get("description", ""),
                    "support_type": offre["support_type"],
                    "category": offre["category"],
                    "unit_price": offre["unit_price"],
                    "is_active": True,
                    "is_visible": True,
                    "start_date": timezone.now().date(),
                    "audio_durations": offre.get("audio_durations", ""),
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Offre {obj.name} {'créée' if created else 'existante'}"
                )
            )
            offre_instances.append(obj)

        options = [
            {
                "offer": offre_instances[0],
                "name": "Voix féminine",
                "value": "Oui",
                "additional_price": 1000,
            },
            {
                "offer": offre_instances[1],
                "name": "Voix masculine",
                "value": "Oui",
                "additional_price": 800,
            },
            {
                "offer": offre_instances[2],
                "name": "Musique de fond",
                "value": "Oui",
                "additional_price": 2000,
            },
            {
                "offer": offre_instances[3],
                "name": "Animation",
                "value": "Oui",
                "additional_price": 3000,
            },
            {
                "offer": offre_instances[4],
                "name": "Ciblage",
                "value": "Par pays",
                "additional_price": 2000,
            },
            {
                "offer": offre_instances[6],
                "name": "Skippable",
                "value": "Non",
                "additional_price": 1000,
            },
        ]

        for opt in options:
            obj, created = OfferOption.objects.get_or_create(**opt)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Option {obj.name} pour {obj.offer.name} {'créée' if created else 'existante'}"
                )
            )

        emplacements = [
            {
                "offer": offre_instances[3],
                "name": "Header principal",
                "available_slots": 3,
                "price_per_slot": 10000,
            },
            {
                "offer": offre_instances[4],
                "name": "Bas de page",
                "available_slots": 4,
                "price_per_slot": 8000,
            },
            {
                "offer": offre_instances[6],
                "name": "Page d'accueil mobile",
                "available_slots": 5,
                "price_per_slot": 7000,
            },
        ]

        for emp in emplacements:
            obj, created = AdPlacement.objects.get_or_create(**emp)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Emplacement {obj.name} pour {obj.offer.name} {'créé' if created else 'existant'}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS("✔ Données enrichies seedées avec succès.")
        )

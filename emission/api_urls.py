from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from emission.views import EmissionViewSet
from emission.views import FridayEditorialViewSet
from emission.views import PoadcastViewSet
from emission.views import SubEmissionViewSet
from emission.views import EpisodeViewSet

router = DefaultRouter()
router.register(r"emissions", EmissionViewSet, basename="emission")
router.register(r"sous-emissions", SubEmissionViewSet, basename="subemission")
router.register(r"editos-vendredi", FridayEditorialViewSet, basename="editorial")
router.register(r"poadcasts", PoadcastViewSet, basename="poadcast")
router.register(r"episode",EpisodeViewSet , basename="episode")

urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from miscellaneous.views import AboutViewSet
from miscellaneous.views import ContactAPIView
from miscellaneous.views import CookieViewSet
from miscellaneous.views import GeneralConditionViewSet
from miscellaneous.views import LegalNoticeViewSet
from miscellaneous.views import PersonalDataViewSet
from miscellaneous.views import PublicityViewSet
from miscellaneous.views import ServiceViewSet
from miscellaneous.views import SliderViewSet
from miscellaneous.views import VideoViewSet

router = DefaultRouter()
router.register(r"about", AboutViewSet)
router.register(r"cookies", CookieViewSet)
router.register(r"personal-data", PersonalDataViewSet)
router.register(r"legal-notice", LegalNoticeViewSet)
router.register(r"general-conditions", GeneralConditionViewSet)
router.register(r"publicities", PublicityViewSet)
router.register(r"sliders", SliderViewSet)
router.register(r"videos", VideoViewSet)
router.register(r"services", ServiceViewSet, basename="service")

urlpatterns = [
    path("", include(router.urls)),
    path("contact/", ContactAPIView.as_view(), name="contact-api"),
]

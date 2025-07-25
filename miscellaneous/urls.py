from django.urls import path

from miscellaneous.views import AboutPageView
from miscellaneous.views import ContactPageView
from miscellaneous.views import CookiePageView
from miscellaneous.views import ERadioPageView
from miscellaneous.views import GamePageView
from miscellaneous.views import GCUPageView
from miscellaneous.views import HomePageView
from miscellaneous.views import LegalNoticePageView
from miscellaneous.views import PersonalDataPageView
from miscellaneous.views import PublicityView
from miscellaneous.views import VideoDetailView
from miscellaneous.views import VideoListView

app_name = "miscellaneous"
urlpatterns = [
    path("", HomePageView.as_view(), name="index"),
    path("a-propos/", AboutPageView.as_view(), name="a-propos"),
    path("mentions-legales/", LegalNoticePageView.as_view(), name="mention-legale"),
    path("cookie/", CookiePageView.as_view(), name="cookie"),
    path(
        "politique-donnees-personnelles/",
        PersonalDataPageView.as_view(),
        name="donnee-personnelle",
    ),
    path("condition-generale/", GCUPageView.as_view(), name="condition-generale"),
    path("publicité/", PublicityView.as_view(), name="publicite"),
    path("jeux/", GamePageView.as_view(), name="e-jeux"),
    path("contact/", ContactPageView.as_view(), name="contact"),
    path("e-radio/", ERadioPageView.as_view(), name="radio"),
    path("video/", VideoListView.as_view(), name="video"),
    path("video/<slug:slug>/", VideoDetailView.as_view(), name="video-detail"),
]

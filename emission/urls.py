from django.urls import path

from emission.views import EmissionDetailView
from emission.views import EmissionListView
from emission.views import FridayEditorialDetailView
from emission.views import SubEmissionDetailView

app_name = "emissions"
urlpatterns = [
    path("", EmissionListView.as_view(), name="emission_list"),
    path("<slug:slug_uri>/", EmissionDetailView.as_view(), name="emission_detail"),
    path(
        "<slug:slug_uri>/", SubEmissionDetailView.as_view(), name="sous_emission_detail"
    ),
    path("<slug:slug_uri>/", FridayEditorialDetailView.as_view(), name="edito_detail"),
]

from django.urls import path

from actuality.views import ActualityDetailView
from actuality.views import ActualityListView

app_name = "actuality"
urlpatterns = [
    path("", ActualityListView.as_view(), name="actuality_list"),
    path("<slug:slug_uri>/", ActualityDetailView.as_view(), name="actuality_detail"),
]

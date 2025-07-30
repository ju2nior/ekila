from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import ListView
from rest_framework import viewsets
from .serializers import EpisodeSerializer, CategorieSerializer
from emission.models import Emission
from emission.models import FridayEditorial
from emission.models import Poadcast, Episode, Categorie
from emission.models import SubEmission
from emission.serializers import EmissionSerializer
from emission.serializers import FridayEditorialSerializer
from emission.serializers import PoadcastSerializer
from emission.serializers import SubEmissionSerializer


class EmissionListView(ListView):
    model = Emission
    template_name = "emissions.html"
    context_object_name = "page_emission"
    paginate_by = 8

    def get_queryset(self):
        return self.model._default_manager.filter(draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            poadcasts = Paginator(Poadcast.objects.all(), 12)
            context["page_poad"] = poadcasts.get_page(self.request.GET.get("page"))
        except Poadcast.DoesNotExist:
            raise Http404(_("Poadcasts not found"))

        try:
            edito_list = FridayEditorial.objects.all()
            for value in edito_list:
                if value.is_still_available():
                    value.delete()
            context["edito"] = edito_list
        except FridayEditorial.DoesNotExist:
            raise Http404(_("Editos not found"))

        return context


class EmissionDetailView(DetailView):
    model = Emission
    template_name = "emissionSelected.html"
    context_object_name = "emission"

    def get_object(self):
        slug = self.kwargs.get("slug_uri")
        return get_object_or_404(
            self.model._default_manager.select_related(), slug_uri=slug
        )


class SubEmissionDetailView(DetailView):
    model = SubEmission
    template_name = "sousEmission.html"
    context_object_name = "sous_emission"

    def get_object(self):
        slug = self.kwargs.get("slug_uri")
        return get_object_or_404(
            self.model._default_manager.select_related(), slug_uri=slug
        )


class FridayEditorialDetailView(DetailView):
    model = FridayEditorial
    template_name = "edito.html"
    context_object_name = "edito"

    def get_object(self):
        slug = self.kwargs.get("slug_uri")
        return get_object_or_404(
            self.model._default_manager.select_related(), slug_uri=slug
        )


class EmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Emission.objects.all()
    serializer_class = EmissionSerializer


class SubEmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubEmission.objects.all()
    serializer_class = SubEmissionSerializer


class FridayEditorialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FridayEditorial.objects.all()
    serializer_class = FridayEditorialSerializer

class PoadcastViewSet(viewsets.ReadOnlyModelViewSet):
  
    queryset = Poadcast.objects.select_related("categorie").all().order_by("-created_at")
    serializer_class = PoadcastSerializer


class CategorieViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Categorie.objects.all().order_by("nom")
    serializer_class = CategorieSerializer


class EpisodeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        podcast_id = self.request.query_params.get('podcast_id')
        if podcast_id:
            return Episode.objects.filter(podcast__id=podcast_id).order_by("-created_at")
        return Episode.objects.all().order_by("-created_at")

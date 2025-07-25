from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView
from rest_framework.viewsets import ReadOnlyModelViewSet

from actuality.models import Actuality
from actuality.serializers import ActualitySerializer


class ActualityListView(ListView):
    model = Actuality
    template_name = "actualite.html"
    context_object_name = "paginated_data"
    paginate_by = 8
    queryset = Actuality.objects.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = {
            "actu_afrique": "Afrique",
            "actu_amerique": "Amerique",
            "actu_asie": "Asie",
            "actu_europe": "Europe",
            "actu_oceanie": "Oceanie",
            "actu_antarctique": "Antarctique",
            
        }

        types = {
            "type_politique": "politique",
            "type_economie": "economie",
            "type_international": "international",
            "type_societe": "societe",
            "type_sante": "sante",
            "type_technologie": "technologie",
            "type_environnement": "environnement",
            "type_culture": "culture",
            "type_sports": "sports",
            "type_sciences": "sciences",
            "type_education": "education",
            "type_justice": "justice",
            "type_evenement": "evenement",
            "type_innovation": "innovation",
            "type_podcast": "podcast",
    }
        paginated_data = {}

        for key, category in categories.items():
            actu_category = self.queryset.filter(category=category)
            paginator = Paginator(actu_category, self.paginate_by)
            paginated_data[key] = paginator.get_page(self.request.GET.get("page"))


        type_paginated = {}

        for key, type_value in types.items():
            type_queryset = Actuality.objects.filter(type=type_value).order_by("-created_at")
            type_paginated[key] = Paginator(type_queryset, self.paginate_by).get_page(
                self.request.GET.get(f"page_{key}")
            )
        context["paginated_data"] = paginated_data
        
        context["paginated_types"] = type_paginated
        return context


class ActualityDetailView(DetailView):
    model = Actuality
    template_name = "actuSelected.html"
    context_object_name = "actu"

    def get_object(self):
        slug = self.kwargs.get("slug_uri")
        return get_object_or_404(Actuality.objects.select_related(), slug_uri=slug)


class ActualityViewSet(ReadOnlyModelViewSet):
    queryset = Actuality.objects.all()
    serializer_class = ActualitySerializer

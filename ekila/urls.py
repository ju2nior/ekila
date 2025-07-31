from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="API Ekila",
        default_version="v1",
        description="API pour la gestion des offres publicitaires et paiements",
        terms_of_service="https://ekila.com/terms/",
        contact=openapi.Contact(email="contact@ekila.com"),
        license=openapi.License(name="License Propriétaire"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("actualites/", include("actuality.urls")),
    path("emission/", include("emission.urls")),
    path("", include("miscellaneous.urls")),
    path("api/", include("actuality.api_urls")),
    path("api/miscellaneous/", include("miscellaneous.api_urls")),
    path("api/", include("emission.api_urls")),
    path("api/tarif/", include("tarif.urls")),
    path('api/evenement/', include('evenslide.api_urls')),
    path(
        "api/docs/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"
    ),

    # path("evenement/", include("evenslide.urls")),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Ekila Radio Administration"
admin.site.site_title = "Ekila Administration"
admin.site.index_title = "Ekila Radio Dashboard"

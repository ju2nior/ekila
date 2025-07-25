from rest_framework.routers import DefaultRouter
from django.urls import path, include 
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .views import EvenementViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



router = DefaultRouter()
router.register(r'evenements', EvenementViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="API Ekila",
        default_version="v1",
        description="API pour la gestion des événements",
        terms_of_service="https://ekila.com/terms/",
        contact=openapi.Contact(email="contact@ekila.com"),
        license=openapi.License(name="License Propriétaire"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    
    
    path('', include(router.urls)),  

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

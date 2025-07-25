from rest_framework.routers import DefaultRouter

from actuality.views import ActualityViewSet

router = DefaultRouter()
router.register(r"actualities", ActualityViewSet)

urlpatterns = router.urls

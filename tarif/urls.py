from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from tarif.views import AdPlacementViewSet
from tarif.views import CartAPIView
from tarif.views import LoginView
from tarif.views import LogoutView
from tarif.views import OfferCategoryViewSet
from tarif.views import OfferListView
from tarif.views import OfferOptionViewSet
from tarif.views import OrderViewSet
from tarif.views import PaymentCallbackView
from tarif.views import PaymentViewSet
from tarif.views import RegisterView
from tarif.views import UserProfileView

router = DefaultRouter()
router.register(r"categories", OfferCategoryViewSet)
router.register(r"options", OfferOptionViewSet)
router.register(r"placements", AdPlacementViewSet)
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("offers/", OfferListView.as_view(), name="offer-list"),
    path("cart/", CartAPIView.as_view(), name="cart"),
    path("payment/callback/", PaymentCallbackView.as_view(), name="payment-callback"),
]

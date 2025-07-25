from django.contrib import admin

from tarif.models import AdPlacement
from tarif.models import AdvertisingOffer
from tarif.models import OfferCategory
from tarif.models import OfferOption
from tarif.models import Order
from tarif.models import Payment

admin.site.register(OfferCategory)
admin.site.register(AdvertisingOffer)
admin.site.register(OfferOption)
admin.site.register(AdPlacement)
admin.site.register(Order)
admin.site.register(Payment)

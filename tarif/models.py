from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class OfferCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    description =RichTextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Offer Category")
        verbose_name_plural = _("Offer Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name


class AdvertisingOffer(models.Model):
    class SupportType(models.TextChoices):
        AUDIO = "audio", _("Audio")
        WEBSITE = "site", _("Website Carousel")
        MOBILE = "mobile", _("Mobile Carousel")
        POPUP = "popup", _("Popup")

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = RichTextField(_("Description"), blank=True)
    support_type = models.CharField(
        max_length=20, choices=SupportType.choices, verbose_name=_("Support Type")
    )
    category = models.ForeignKey(
        OfferCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offers",
        verbose_name=_("Category"),
    )
    unit_price = models.PositiveIntegerField(
        help_text=_("Price in FCFA"), verbose_name=_("Unit Price")
    )
    is_active = models.BooleanField(
        default=True, help_text=_("Is the offer active?"), verbose_name=_("Active")
    )
    start_date = models.DateField(null=True, blank=True, verbose_name=_("Start Date"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"))
    is_visible = models.BooleanField(
        default=True, verbose_name=_("Visible"), help_text=_("Visible on the platform")
    )
    audio_durations = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_("Audio Durations"),
        help_text=_("Duration of audio spots (e.g., 20s, 30s)"),
    )

    class Meta:
        verbose_name = _("Advertising Offer")
        verbose_name_plural = _("Advertising Offers")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_support_type_display()})"


class OfferOption(models.Model):
    offer = models.ForeignKey(
        AdvertisingOffer,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name=_("Advertising Offer"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Option Name"))
    value = models.CharField(max_length=50, verbose_name=_("Value"))
    additional_price = models.PositiveIntegerField(
        default=0,
        help_text=_("Extra price for this option"),
        verbose_name=_("Additional Price"),
    )

    class Meta:
        verbose_name = _("Offer Option")
        verbose_name_plural = _("Offer Options")

    def __str__(self):
        return f"{self.name}: {self.value} (+{self.additional_price} FCFA)"


class AdPlacement(models.Model):
    offer = models.ForeignKey(
        AdvertisingOffer,
        on_delete=models.CASCADE,
        related_name="placements",
        verbose_name=_("Advertising Offer"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Placement Name"))
    available_slots = models.PositiveIntegerField(
        default=0, verbose_name=_("Available Slots")
    )
    price_per_slot = models.PositiveIntegerField(verbose_name=_("Price per Slot"))

    class Meta:
        verbose_name = _("Ad Placement")
        verbose_name_plural = _("Ad Placements")

    def __str__(self):
        return f"{self.name} ({self.available_slots} slots available)"


class Order(models.Model):
    reference = models.CharField(
        max_length=100, unique=True, verbose_name=_("Reference")
    )
    description =  RichTextField(_("Description"), blank=True)
    amount = models.PositiveIntegerField(verbose_name=_("Amount (FCFA)"))
    is_paid = models.BooleanField(default=False, verbose_name=_("Paid"))
    cart = models.JSONField(default=list, verbose_name=_("Cart Items"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, verbose_name=_("User")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.reference} - {self.amount} FCFA"


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    ACCEPTED = "ACCEPTED", _("Accepted")
    REFUSED = "REFUSED", _("Refused")
    CANCELLED = "CANCELLED", _("Cancelled")


class Payment(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment", verbose_name=_("Order")
    )
    transaction_id = models.CharField(
        max_length=100, unique=True, verbose_name=_("Transaction ID")
    )
    amount = models.PositiveIntegerField(verbose_name=_("Amount"))
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name=_("Status"),
    )
    response_data = models.JSONField(
        blank=True, null=True, verbose_name=_("Response Data")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.get_status_display()}"

    def update_status(self) -> dict:
        from utils.cinetpay import CinetPay

        cp = CinetPay()
        result = cp.verify_payment(self.transaction_id)

        if result.get("code") == "00":
            self.status = result["data"]["status"]
            self.response_data = result["data"]
            self.save()

            if self.status == PaymentStatus.ACCEPTED:
                self.order.is_paid = True
                self.order.save()

        return result

from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from actuality.models import Actuality
from emission.models import Poadcast
from miscellaneous.forms import ContactForm
from miscellaneous.models import About
from miscellaneous.models import Cookie
from miscellaneous.models import GeneralCondition
from miscellaneous.models import LegalNotice
from miscellaneous.models import PersonalData
from miscellaneous.models import Publicity
from miscellaneous.models import Service
from miscellaneous.models import Slider
from miscellaneous.models import Video
from miscellaneous.serializers import AboutSerializer
from miscellaneous.serializers import ContactSerializer
from miscellaneous.serializers import CookieSerializer
from miscellaneous.serializers import GeneralConditionSerializer
from miscellaneous.serializers import LegalNoticeSerializer
from miscellaneous.serializers import PersonalDataSerializer
from miscellaneous.serializers import PublicitySerializer
from miscellaneous.serializers import ServiceSerializer
from miscellaneous.serializers import SliderSerializer
from miscellaneous.serializers import VideoSerializer


class BasePageView(TemplateView):
    model = None
    context_key = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.model and self.context_key:
            context[self.context_key] = self.model.objects.first()
        return context


class AboutPageView(BasePageView):
    template_name = "a-propos.html"
    model = About
    context_key = "propos"


class CookiePageView(BasePageView):
    template_name = "cookie.html"
    model = Cookie
    context_key = "cookie"


class LegalNoticePageView(BasePageView):
    template_name = "mention_legale.html"
    model = LegalNotice
    context_key = "notice"


class PersonalDataPageView(BasePageView):
    template_name = "donnee_perso.html"
    model = PersonalData
    context_key = "donnee"


class GCUPageView(BasePageView):
    template_name = "gcu.html"
    model = GeneralCondition
    context_key = "condition"


class PublicityView(BasePageView):
    template_name = "publicite.html"
    model = Publicity
    context_key = "publicity"


class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sliders"] = Slider.objects.filter(draft=False)
        context["welcome_slider"] = Slider.objects.filter(
            is_welcome=True, draft=False
        ).first()
        context["actuality"] = Actuality.objects.filter(is_up_to_date=True).order_by(
            "created_at"
        )[:4]
        context["poadcast"] = Poadcast.objects.filter()[:4]
        return context


class GamePageView(TemplateView):
    # TODO :)
    template_name = "jeux.html"


class ERadioPageView(TemplateView):
    template_name = "e-radio.html"


class ContactPageView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("miscellaneous:contact")
    success_message = _("Votre message a été envoyé avec succès 😊!")

    def form_valid(self, form):
        is_message_send = form.send_email()
        if is_message_send:
            messages.success(self.request, self.success_message)
        else:
            messages.error(
                self.request,
                _(
                    "Une erreur est survenu lors de l'envoi du message, veuillez reessayer plutard😊!"
                ),
            )
        return super().form_valid(form)


class VideoListView(ListView):
    model = Video
    template_name = "video.html"
    context_object_name = "videos"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ekila_musique_videos = Video.objects.filter(
            category="videos Ekila Musique"
        ).order_by("title")
        ekila_radio_videos = Video.objects.filter(
            category="videos Ekila Radio"
        ).order_by("title")

        paginator_musique = Paginator(ekila_musique_videos, self.paginate_by)
        paginator_radio = Paginator(ekila_radio_videos, self.paginate_by)

        page_number_musique = self.request.GET.get("page_musique", 1)
        page_number_radio = self.request.GET.get("page_radio", 1)

        context["ekila_musique_videos"] = paginator_musique.get_page(
            page_number_musique
        )
        context["ekila_radio_videos"] = paginator_radio.get_page(page_number_radio)

        return context


class VideoDetailView(DetailView):
    model = Video
    template_name = "video-detail.html"
    context_object_name = "video"
    slug_url_kwarg = "slug"


class AboutViewSet(ReadOnlyModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer


class CookieViewSet(ReadOnlyModelViewSet):
    queryset = Cookie.objects.all()
    serializer_class = CookieSerializer


class PersonalDataViewSet(ReadOnlyModelViewSet):
    queryset = PersonalData.objects.all()
    serializer_class = PersonalDataSerializer


class LegalNoticeViewSet(ReadOnlyModelViewSet):
    queryset = LegalNotice.objects.all()
    serializer_class = LegalNoticeSerializer


class GeneralConditionViewSet(ReadOnlyModelViewSet):
    queryset = GeneralCondition.objects.all()
    serializer_class = GeneralConditionSerializer


class PublicityViewSet(ReadOnlyModelViewSet):
    queryset = Publicity.objects.all()
    serializer_class = PublicitySerializer


class SliderViewSet(ReadOnlyModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer


class VideoViewSet(ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class ServiceViewSet(ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ContactAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            try:
                service_id = data.get("service_id")
                service = Service.objects.get(id=service_id)
                destinataire = service.email

                message_content = f"""
Nom : {data['nom']}
Prénom : {data['prenom']}
Email : {data['email']}
Téléphone : {data['telephone']}
Service : {service.name}
Message :
{data['message']}
"""

                email = EmailMessage(
                    subject=f"Nouveau message de {data['prenom']} {data['nom']}",
                    body=message_content,
                    from_email=data["email"],
                    to=[destinataire],
                )

                if "fichier" in request.FILES:
                    fichier = request.FILES["fichier"]
                    email.attach(fichier.name, fichier.read(), fichier.content_type)

                email.send(fail_silently=False)

                return Response(
                    {"success": "Message envoyé"}, status=status.HTTP_200_OK
                )

            except Service.DoesNotExist:
                return Response(
                    {"error": "Le service sélectionné est introuvable."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

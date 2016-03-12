from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from api.models import Sighting

from api.models import SightingFAQ

class HomePageView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['new_sighting'] = reverse('new_sighting')
        return context

class FAQView(ListView):
    template_name = "faq.html"
    model = SightingFAQ


class SightingExpertCommentsView(ListView):
    template_name = "sighting_expert_comments.html"


class SightingView(DetailView):
    template_name = "sighting.html"
    pk_url_kwarg= "sighting_id"
    model= Sighting


class SightingsView(ListView):
    template_name = "sightings.html"
    model = Sighting# Defino el modelo que utilizo
    context_object_name = "sightings_list"# Defino la lista donde se cargan los objetos del modelo
    paginate_by = 50  # Control de la paginacion

    def get_queryset(self, **kwargs):
        return Sighting.objects.all()

class SightQuestionView(DetailView):
    template_name = "sight_question.html"


class LocationsPageView(TemplateView):
    template_name = "locations.html"


class SightingCommentsView(ListView):
    template_name = "sighting_comments.html"


class SightExpertCommentView(DetailView):
    template_name = "sight_expert_comment.html"

class NewSightingView(TemplateView):
    template_name = "new_sighting.html"

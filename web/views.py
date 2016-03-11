from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = "home.html"

class FAQView(TemplateView):
    template_name = "faq.html"

class SightingExpertCommentsView(TemplateView):
    template_name = "sighting_expert_comments.html"

class SightingView(TemplateView):
    template_name = "sighting.html"

class SightingsView(TemplateView):
    template_name = "sightings.html"


class SightQuestionView(TemplateView):
    template_name = "sight_question.html"

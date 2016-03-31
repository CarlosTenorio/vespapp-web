from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.context_processors import csrf

from api.models import Sighting
from api.models import SightingFAQ
from api.models import Sighting
from api.models import UserComment

from web.forms import SightingForm
from web.forms import PictureForm


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


class SightingsView(ListView):
    template_name = "sightings.html"
    model = Sighting  # Defino el modelo que utilizo
    context_object_name = "sightings_list"  # Defino la lista donde se cargan los objetos del modelo
    paginate_by = 50  # Control de la paginacion

    def get_queryset(self, **kwargs):
        return Sighting.objects.all()


class SightingView(DetailView):
    template_name = "sighting.html"
    pk_url_kwarg = 'sighting_id'
    model = Sighting

    def get_queryset(self, **kwargs):
        return Sighting.objects.all()


class SightQuestionView(DetailView):
    template_name = "sight_question.html"


class LocationsPageView(TemplateView):
    template_name = "locations.html"


class SightExpertCommentView(DetailView):
    template_name = "sight_expert_comment.html"


class NewSightingView(TemplateView):
    #template_name = "new_sighting.html"

    def new_sighting(request):
        if request.POST:
            form_sighting = SightingForm(request.POST)
            form_picture = PictureForm(request.POST, request.FILES)
            print(form_sighting)
            print(request.POST)
            print(form_picture)
            print(request.FILES)

            if form_sighting.is_valid() and form_picture.is_valid():
                sighting_id = form_sighting.save()
                picture_id = form_picture.save(commit=False)
                picture_id.sighting = sighting_id
                picture_id.save()

                """free_text = form.cleaned_data['free_text']

                sighting_obj = Sighting(type=type, free_text=free_text)
                sighting_obj.save()"""

                return HttpResponseRedirect('')
        else:
            form_sighting = SightingForm()

        args = {}
        args.update(csrf(request))

        args['form'] = form_sighting

        return render_to_response('new_sighting.html', args)



class SightingCommentView(DetailView):
    template_name = "sighting_comment.html"
    template_name_field = 'object'
    model = UserComment

    def get_object(self, queryset=None):
        sighting_id = self.kwargs.get('sighting_id')
        comment_id = self.kwargs.get('comment_id')

        comment = UserComment.objects.get(pk=comment_id)

        if str(comment.sighting.id) != str(sighting_id):
            return None

        return comment


class SightingCommentsView(ListView):
    template_name = "sighting.html"
    model = UserComment  # Defino el modelo que utilizo
    context_object_name = "user_comment_list"  # Defino la lista donde se cargan los objetos del modelo

    def get_queryset(self, **kwargs):
        return UserComment.objects.all()

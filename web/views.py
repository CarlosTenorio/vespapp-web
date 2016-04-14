from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from api.models import Sighting
from api.models import Location
from api.models import Picture
from api.models import SightingFAQ
from api.models import UserComment
from api.models import Question
from api.models import Answer

from web.forms import SightingForm
from web.forms import QuestionForm


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


class LocationsPageView(TemplateView):
    template_name = "locations.html"


class SightExpertCommentView(DetailView):
    template_name = "sight_expert_comment.html"


class SightQuestionView(TemplateView):
    @csrf_exempt
    def sight_question(request, sighting_id, question_order):

        s = Sighting.objects.get(id=sighting_id)   

        if request.POST:
            form_question = QuestionForm(request.POST)    
            # print("FORM_QUESTION")
            # print("")
            # print(form_question) 
            # print("")
            # print("REQUEST.POST")
            # print(request.POST)
            # print("")
            # print("REQUEST.FILES")
            # print(request.FILES)
            # print("")
            # print("Es valido?")
            # print(form_question.is_valid())  
            # print("");

            if form_question.is_valid():
                if request.FILES == None:
                    raise Http404("No objects uploaded")    

                myArray = request.POST.pop('value')

                for x in myArray:
                    s.answers.add(x)

                q = Question.objects.filter(order=int(question_order)+1, sighting_type=s.type)
                if q.exists():
                    print("")
                    print("EXISTE")
                    url = reverse('sight_question', kwargs={'sighting_id': sighting_id, 'question_order': int(question_order)+1})
                    return HttpResponseRedirect(url)
                else:
                    return HttpResponseRedirect('')
                    
                # return redirect(reverse('home'))

        else:
            form_question = QuestionForm()

        context = {
            'sighting': Sighting.objects.get(id=sighting_id),
            'question': Question.objects.get(order=question_order, sighting_type=s.type),
            'answer': Answer.objects.all()
        }
        return render_to_response('sight_question.html', context=context)



class NewSightingView(TemplateView):
    #template_name = "new_sighting.html"

    @csrf_exempt
    def new_sighting(request):
        context = {
            'locations': Location.objects.all()
        }

        if request.POST:
            form_sighting = SightingForm(request.POST)
            #form_picture = PictureForm(request.POST, request.FILES)
            print("")
            print(form_sighting)
            print("")
            print(request.POST)
            print("")
            print(request.FILES)
            print("")
            print(form_sighting.is_valid())
            print("")

            if form_sighting.is_valid():
                if request.FILES == None:
                    raise Http404("No objects uploaded")

                sighting_id = form_sighting.save(commit=False)
                sighting_id.source = 'Web'
                sighting_id.save()

                uploaded_files = [request.FILES.get('file[%d]' % i)
                    for i in range(0, len(request.FILES))]

                for f in uploaded_files:
                    picture_id = Picture()
                    picture_id.sighting = sighting_id
                    picture_id.file.save(f.name, f)
                    picture_id.save()              

                return HttpResponseRedirect('')
        else:
            form_sighting = SightingForm()

        return render_to_response('new_sighting.html', context=context)


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
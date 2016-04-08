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
from api.models import UserProfile

from web.forms import SightingForm
from web.forms import RegistroUserForm

from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.urlresolvers import reverse



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
    pk_url_kwarg = 'sighting_id'
    model = Question

    def get_queryset(self, **kwargs):
        return Question.objects.all()


class LocationsPageView(TemplateView):
    template_name = "locations.html"


class SightExpertCommentView(DetailView):
    template_name = "sight_expert_comment.html"


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


def registro_usuario_view(request):
    if request.method == 'POST':
        # Si el method es post, obtenemos los datos del formulario
        form = RegistroUserForm(request.POST, request.FILES)

        # Comprobamos si el formulario es valido
        if form.is_valid():
            # En caso de ser valido, obtenemos los datos del formulario.
            # form.cleaned_data obtiene los datos limpios y los pone en un
            # diccionario con pares clave/valor, donde clave es el nombre del campo
            # del formulario y el valor es el valor si existe.
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            photo = cleaned_data.get('photo')
            # E instanciamos un objeto User, con el username y password
            user_model = User.objects.create_user(username=username, password=password)
            # Añadimos el email
            user_model.email = email
            # Y guardamos el objeto, esto guardara los datos en la db.
            user_model.save()
            # Ahora, creamos un objeto UserProfile, aunque no haya incluido
            # una imagen, ya quedara la referencia creada en la db.
            user_profile = UserProfile()
            # Al campo user le asignamos el objeto user_model
            user_profile.user = user_model
            # y le asignamos la photo (el campo, permite datos null)
            user_profile.photo = photo
            # Por ultimo, guardamos tambien el objeto UserProfile
            user_profile.save()
            # Ahora, redireccionamos a la pagina gracias.html
            # Pero lo hacemos con un redirect.
            return redirect(reverse('gracias', kwargs={'username': username}))
    else:
        # Si el mthod es GET, instanciamos un objeto RegistroUserForm vacio
        form = RegistroUserForm()
    # Creamos el contexto
    context = {'form': form}
    # Y mostramos los datos
    return render(request, 'registration_form.html', context)

def gracias_view(request, username):
    return render(request, 'gracias.html', {'username': username})
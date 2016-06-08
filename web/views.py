from django.shortcuts import render
from django.shortcuts import render_to_response 
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404  
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

import json

from api.models import Sighting
from api.models import Location
from api.models import Picture
from api.models import SightingInfo
from api.models import UserComment
from api.models import Question
from api.models import Answer
from api.models import UserProfile

from web.forms import SightingForm
from web.forms import QuestionForm
from web.forms import CommentSightingForm
from web.forms import SightingForm
from web.forms import SignupUserForm
from web.forms import UserProfileForm
from web.forms import PasswordProfileForm
from web.forms import PhotoProfileForm
from web.forms import ContactForm



class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['new_sighting'] = reverse('new_sighting')
        return context


class NewSightingView(TemplateView):

    @csrf_exempt
    def new_sighting(request):

        if request.POST:

            form_sighting = SightingForm(request.POST)

            if form_sighting.is_valid():
                if request.FILES == None:
                    raise Http404("No objects uploaded")

                sighting_id = form_sighting.save(commit=False)
                sighting_id.source = 'web'
                if request.user.is_authenticated():
                    sighting_id.contact = request.user.email
                    user = User.objects.get(username=request.user.username)
                    sighting_id.user = user
                sighting_id.save()

                uploaded_files = [request.FILES.get('file[%d]' % i)
                    for i in range(0, len(request.FILES))]

                for f in uploaded_files:
                    picture_id = Picture()
                    picture_id.sighting = sighting_id
                    picture_id.file.save(f.name, f)
                    picture_id.save()

                request.session['session_id'] = sighting_id.id   
                request.session['question_order'] = 0  

                return HttpResponse(sighting_id.pk)
        else:
            form_sighting = SightingForm()

        context = {
            'locations': Location.objects.all()
        }

        return render(request, 'new_sighting.html', context=context)


class SightingsView(ListView):
    template_name = "sightings.html"
    model = Sighting  # Defino el modelo que utilizo
    context_object_name = "sightings_list"  # Defino la lista donde se cargan los objetos del modelo
    paginate_by = 50  # Control de la paginacion

    def get_queryset(self, **kwargs):
        if self.request.user.is_authenticated():
            user = User.objects.get(username=self.request.user.username)
            return Sighting.objects.filter(Q(public=True) | Q(user=user))
        else:
            return Sighting.objects.filter(public=True)


class SightingView(TemplateView):

    def sighting_view(request, sighting_id):

        if request.POST:
            form_comment = CommentSightingForm(request.POST)
            if form_comment.is_valid():   
                comment_id = form_comment.save(commit=False)
                sighting = Sighting.objects.get(id=int(sighting_id))
                comment_id.sighting = sighting
                user = User.objects.get(username=request.user.username)
                comment_id.user = user
                comment_id.save()

                return HttpResponseRedirect('')                   
        else:
            form_comment = CommentSightingForm()

        try:
            context = {
                'sighting': Sighting.objects.get(id=int(sighting_id)),
                'form_comment': form_comment
            }
        except Sighting.DoesNotExist:
            context = {
                'sighting': None
            }

        return render_to_response('sighting.html', context=context, context_instance=RequestContext(request))


class SightQuestionView(TemplateView):

    @csrf_exempt
    def sight_question(request):

        if "session_id" in request.session:
                    
            sighting_id = request.session['session_id']
            question_order = request.session['question_order'] + 1 

            request.session['question_order'] = question_order

            s = Sighting.objects.get(id=sighting_id)   

            if request.POST:
                form_question = QuestionForm(request.POST)   

                if form_question.is_valid():
                    if request.FILES == None:
                        raise Http404("No objects uploaded")    

                    myArray = request.POST.pop('value')

                    for x in myArray:
                        s.answers.add(x)

                    q = Question.objects.filter(order=int(question_order), sighting_type=s.type)
                    if q.exists():           
                        #Subtracting one so that the next if it comes from one form to add beginning work properly
                        question_order = request.session['question_order'] - 1                         
                        request.session['question_order'] = question_order
                        url = reverse('sight_question')
                        return HttpResponseRedirect(url)
                    else:
                        message='Regístrate para conocer el estado de tu avispamiento, enviar comentarios y mucho más'    
                        return render(request, 'home.html', {'message': message})      
                else:
                    #if click on next button but not select nothing
                    question_order = request.session['question_order'] - 1                         
                    request.session['question_order'] = question_order
                    url = reverse('sight_question')
                    return HttpResponseRedirect(url)              
            else:
                form_question = QuestionForm()

                q = Question.objects.filter(order=int(question_order), sighting_type=s.type)
                if q.exists():
                    context = {
                        'sighting': Sighting.objects.get(id=sighting_id),
                        'question': Question.objects.get(order=question_order, sighting_type=s.type),
                        'answer': Answer.objects.all()
                    }
                    return render_to_response('sight_question.html', context=context, context_instance=RequestContext(request))
                else:
                    message='Regístrate para conocer el estado de tu avispamiento, enviar comentarios y mucho más'    
                    return render(request, 'home.html', {'message': message})
        else:
            raise Http404


class UserSignupView(TemplateView):

    def signup_user_view(request):
        # Si el usuario esta ya logueado, lo redireccionamos a home
        if request.user.is_authenticated():
            return redirect(reverse('home'))

        if request.method == 'POST':
            # Si el method es post, obtenemos los datos del formulario
            form = SignupUserForm(request.POST, request.FILES)

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

                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                    else:
                        pass
                #if he comes from new_sighting
                if 'session_id' in request.session:
                    sighting_id = request.session['session_id']
                    s = Sighting.objects.get(id=sighting_id)   
                    s.user = user
                    s.save()

                # Ahora, redireccionamos a la pagina home.html
                # Pero lo hacemos con un redirect.
                return redirect(reverse('home'))
        else:
            # Si el mthod es GET, instanciamos un objeto RegistroUserForm vacio
            form = SignupUserForm()

        # Creamos el contexto
        context = {'form': form}

        # Y mostramos los datos
        return render(request, 'signup.html', context)


class UserLoginView(TemplateView):

    def login_view(request):
        # Si el usuario esta ya logueado, lo redireccionamos a home
        if request.user.is_authenticated():
            return redirect(reverse('home'))

        message = ''
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #if he comes from new_sighting
                    if 'session_id' in request.session:
                        sighting_id = request.session['session_id']
                        s = Sighting.objects.get(id=sighting_id)   
                        s.user = user
                        s.save()
                    return redirect(reverse('home'))
                else:
                    pass
            message = 'Nombre de usuario o contraseña no válido'
        return render(request, 'login.html', {'message': message})


class UserLogoutView(TemplateView):

    def logout_view(request):
        logout(request)
        message='Has cerrado sesión. ¡Vuelve pronto!'    
        return render(request, 'home.html', {'message_logout': message})


class UserProfileView(TemplateView):
    
    @login_required
    def edit_profile(request):
        if request.method == 'POST':
            if 'UserProfile' in request.POST:
                userForm = UserProfileForm(request.POST, request=request)
                if userForm.is_valid():
                    request.user.username = userForm.cleaned_data['username']
                    request.user.email = userForm.cleaned_data['email']
                    request.user.save()

                    return redirect(reverse('user_profile'))
                else:
                    passwordForm = PasswordProfileForm(user=request.user)
                    photoForm = PhotoProfileForm()

            elif 'PasswordProfile' in request.POST:
                passwordForm = PasswordProfileForm(request.POST, user=request.user)
                if passwordForm.is_valid():
                    password = passwordForm.cleaned_data['password']
                    request.user.password = make_password(password)
                    request.user.save()

                    user = authenticate(username=request.user.username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                        else:
                            pass

                    return redirect(reverse('user_profile'))
                else:
                    userForm = UserProfileForm(
                        request=request, 
                        initial={'email': request.user.email, 'username': request.user.username})
                    photoForm = PhotoProfileForm()

            elif 'PhotoProfile' in request.POST:
                photoForm = PhotoProfileForm(request.POST, request.FILES)

                if photoForm.is_valid():
                    cleaned_data = photoForm.cleaned_data
                    photo = cleaned_data.get('photo')

                    user = User.objects.get(username=request.user.username)
                    user_profile = UserProfile.objects.get(user=user)
                    user_profile.photo = photo
                    user_profile.save()

                    return redirect(reverse('user_profile'))  
                else:
                    userForm = UserProfileForm(
                        request=request, 
                        initial={'email': request.user.email, 'username': request.user.username})
                    passwordForm = PasswordProfileForm()

        else:
            userForm = UserProfileForm(
                request=request, 
                initial={'email': request.user.email, 'username': request.user.username})
            passwordForm = PasswordProfileForm(user=request.user)
            photoForm = PhotoProfileForm()

        user = User.objects.get(username=request.user.username)
        user_profile = UserProfile.objects.get(user=user)
        context = {'userForm': userForm, 
            'passwordForm': passwordForm, 
            'photoForm': photoForm,
            'user_profile': user_profile}    

        return render(request, 'user_profile.html', context)


class InfoView(ListView):
    template_name = "info.html"
    model = SightingInfo


class ContactView(TemplateView):

    def contact_view(request):

        if request.method == 'POST':
            form = ContactForm(request.POST)

            print(request.POST)
            print(form.is_valid())

            if form.is_valid():

                cleaned_data = form.cleaned_data
                username = cleaned_data.get('nameContact')
                email = cleaned_data.get('emailContact')
                phone = cleaned_data.get('phoneContact')
                message = cleaned_data.get('messageContact') 
                        
                send_mail('Contacto Usuario', 
                    'Enviado por: ' + username + 
                    '\n\nCorreo: ' + email + 
                    '\n\nNúmero de teléfono: ' + phone +
                    '\n\nMensaje: ' + message, 
                    settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])

                message='Te contestaremos lo antes posible'    

                context = {'form': form, 'mensaje': message}
                return render(request, 'contact.html', context)
        else:
            form = ContactForm()
  
        context = {'form': form}

        return render(request, 'contact.html', context)


class AboutView(TemplateView):
    template_name = "about.html"


class TeamView(TemplateView):
    template_name = "team.html"

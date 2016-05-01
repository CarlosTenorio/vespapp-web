from django import forms
from api.models import Sighting
from api.models import Answer
from api.models import UserComment
from django.contrib.auth.models import User


class SightingForm(forms.ModelForm):
    
    class Meta:
        model = Sighting
        fields = ('type', 'free_text', 'location', 'lat', 'lng')


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ('value',)


class CommentSightingForm(forms.ModelForm):
    
    class Meta:
        model = UserComment
        fields = ('body',)


class SignupUserForm(forms.Form):

    username = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    photo = forms.ImageField(required=False)

    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual en la db.')
        return email

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2


class UserProfileForm(forms.Form):

    username = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Obtener request"""
        self.request = kwargs.pop('request')
        return super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Comprobar si ha cambiado el email
        current_email = self.request.user.email
        if email != current_email:
            # Si lo ha cambiado, comprobar que no exista en la db.
            exists = User.objects.filter(email=email)
            if exists:
                raise forms.ValidationError('Ya existe un usuario con este email.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        # Comprobar si ha cambiado el username
        current_username = self.request.user.username
        if username != current_username:
            # Si lo ha cambiado, comprobar que no exista en la db.
            exists = User.objects.filter(username=username)
            if exists:
                raise forms.ValidationError('Ya existe un usuario con este nombre.')
        return username


class PasswordProfileForm(forms.Form):

    actual_password = forms.CharField(
        label='Contraseña actual',
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Nueva contraseña',
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repetir contraseña',
        min_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Obtener user"""
        self.user = kwargs.pop('user')
        return super().__init__(*args, **kwargs)

    def clean_actual_password(self):
        """Comprueba que actual_password sean la correcta."""
        actual_password = self.cleaned_data['actual_password']
        if not self.user.check_password(actual_password):
            raise forms.ValidationError('Contraseña inválida')
        return actual_password

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2


class PhotoProfileForm(forms.Form):
    photo = forms.ImageField(required=False)



class ContactForm(forms.Form):

    nameContact = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    emailContact = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    phoneContact = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    messageContact = forms.CharField(
        min_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

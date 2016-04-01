from django import forms
from api.models import Sighting
from api.models import Picture


class SightingForm(forms.ModelForm):
    
    class Meta:
        model = Sighting
        fields = ('type', 'free_text')


class PictureForm(forms.ModelForm):
    
    class Meta:
        model = Picture
        fields = ('file', )
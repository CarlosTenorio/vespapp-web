from django import forms
from api.models import Sighting


class SightingForm(forms.ModelForm):
    
    class Meta:
        model = Sighting
        fields = ('type', 'free_text', 'location')
from django import forms
from api.models import Sighting
from api.models import Answer


class SightingForm(forms.ModelForm):
    
    class Meta:
        model = Sighting
        fields = ('type', 'free_text', 'location')


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ('value',)
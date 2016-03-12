from django import forms

from api.models import Sighting

class MyCreateSightningForm(forms.ModelForm):

    class Meta:
        model = Sighting
        fields = ('type', 'location', 'free_text', 'contact', )

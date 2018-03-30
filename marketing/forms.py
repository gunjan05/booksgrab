from .models import MarketingPreference
from django import forms
from django.http import HttpResponse



class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive Marketing Email', required=False)
    class Meta:
        model = MarketingPreference
        fields = ['subscribed']

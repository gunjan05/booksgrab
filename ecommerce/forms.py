from django import forms

class ContactForm(forms.Form):
    fullname = forms.CharField(label='',widget = forms.TextInput(
                                attrs={'class':'form-control',
                                       'placeholder':'Name'}))
    email = forms.EmailField(label='',widget = forms.EmailInput(
                                attrs={'class':'form-control',
                                       'placeholder':'Email Adrress'}))
    content = forms.CharField(label='',widget = forms.Textarea(
                                attrs={'class':'form-control',
                                       'placeholder':'Type Your Message Here !!',
                                       'rows':'3'}))

from django import forms
from .models import Address, STATES_CHOICES

class AddressForm(forms.Form):
    fullname       = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Fullname'}))
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'1234, Main Street'}))
    address_line_2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Landmark/ Area Name'}))
    state          = forms.CharField(widget=forms.Select(choices=STATES_CHOICES, attrs={'class':'form-control'}))
    city           = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}))
    country        = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}), initial='India', disabled=True)
    postal_code    = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Pincode'}))

    def save(self, billing_profile, address_type):
        data = self.cleaned_data
        address = Address(fullname=data['fullname'],
                          address_line_1=data['address_line_1'],
                          address_line_2=data['address_line_2'],
                          state=data['state'],
                          city=data['city'],
                          country=data['country'],
                          postal_code=data['postal_code'],
                          billing_profile=billing_profile,
                          address_type=address_type )
        address.save()
        return address

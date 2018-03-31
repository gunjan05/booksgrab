from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator
from .signals import user_logged_in
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'mobile_number', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('mobile_number', 'first_name', 'last_name', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class GuestForm(forms.Form):
    first_name = forms.CharField(label='', widget = forms.TextInput(
                                attrs={'class':'form-control first-name',
                                       'placeholder':'First Name*'}))
    last_name = forms.CharField(label='', widget = forms.TextInput(
                                attrs={'class':'form-control last-name',
                                       'placeholder':'Last Name*'}))
    email = forms.EmailField(label='', widget = forms.EmailInput(
                                attrs={'class':'form-control email',
                                       'placeholder':'Email*'}))
    mobile_number = PhoneNumberField(label='', widget=PhoneNumberInternationalFallbackWidget(
                                            attrs={'class':'form-control mobile_no',
                                               'placeholder':'Mobile Number*'}))


class LoginForm(forms.Form):
    email = forms.EmailField(label='', widget = forms.EmailInput(
                                attrs={'class':'form-control',
                                       'placeholder':'Email'}))
    password = forms.CharField(label='',widget = forms.PasswordInput(
                                attrs={'class':'form-control',
                                        'placeholder':'Password'}))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email  = data.get("email")
        password  = data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, 'Invalid Username or Password')
            raise forms.ValidationError('Invalid Credentials')
        login(request, user)
        self.user = user
        user_logged_in.send(user.__class__, instance=user, request=request)
        try:
            del request.session['guest_email_id']
        except:
            pass
        return data

class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control password-1',
                                                                            'placeholder':'Password*'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control password-2',
                                                                            'placeholder':'Confirm Password*'}))
    first_name = forms.CharField(label='', widget = forms.TextInput(
                                attrs={'class':'form-control first-name',
                                       'placeholder':'First Name*'}))
    last_name = forms.CharField(label='', widget = forms.TextInput(
                                attrs={'class':'form-control last-name',
                                       'placeholder':'Last Name*'}))
    email = forms.EmailField(label='', widget = forms.EmailInput(
                                attrs={'class':'form-control email',
                                       'placeholder':'Email*'}))
    mobile_number = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget(
                                            attrs={'class':'form-control mobile_no',
                                               'placeholder':'Mobile Number*'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active = False
        if commit:
            user.save()
        return user

class UserDetailChangeForm(forms.ModelForm):
    first_name = forms.CharField(label='Firstname:' , required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(label='Lastname:' , required=False, widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

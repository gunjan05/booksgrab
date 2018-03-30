from django.shortcuts import render, redirect
import requests
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView, FormView, DetailView, UpdateView
from django.utils.http import is_safe_url
from django.contrib.auth import authenticate, login, get_user_model
from .forms import LoginForm, RegisterForm, GuestForm, UserDetailChangeForm
from .models import GuestDetails
from .signals import user_logged_in
from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_view = 'accounts/user_detail.html'
    def get_object(self):
        return self.request.user

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {'form':form,}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(form.cleaned_data)
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        mobile_number = form.cleaned_data.get('mobile_number')
        new_guest_email = GuestDetails.objects.create(email=email, first_name=first_name, last_name=last_name, mobile_number=mobile_number)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register/')
    return redirect('/register/')

class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    sucess_url = '/'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

    def form_valid(self, form):
         request = self.request
         form = RegisterForm(request.POST or None)
         form.save()
         if request.is_ajax():
            return JsonResponse({"message":"Success"})

    def form_invalid(self, form):
        request = self.request
        errors = RegisterForm(request.POST).errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')


class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Change Your Account Details'
        return context

    def get_success_url(self):
        return reverse("account:home")

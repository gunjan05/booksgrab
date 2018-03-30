from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, get_user_model
from .forms import ContactForm

def home_page(request):
    context = {'title':'Hello World',}
    if request.user.is_authenticated():
        context['premium_content'] = 'This is the premium content that you are viewing'
    return render(request, 'home_page.html',context)

def about_page(request):
    context = {'title':'You are at about page'}
    return render(request, 'home_page.html', context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {'title':'Welcome to Contact Page',
               'form':contact_form
               }
    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({"message":"Success"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    return render(request, 'contact/view.html', context)

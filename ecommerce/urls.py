"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

from .views import home_page, about_page, contact_page
from accounts.views import LoginView, RegisterView, guest_register_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView


urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('accounts.urls', namespace='account')),
    #url(r'^accounts/', RedirectView.as_view(url='/account')),
    url(r'^accounts/', include("accounts.passwords.urls")),
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^register/guest/$', guest_register_view, name='guest_register'),
    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^about/$', about_page, name='about'),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
    url(r'^cart/', include('carts.urls', namespace='cart')),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

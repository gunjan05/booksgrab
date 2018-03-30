from django.conf.urls import url, include
from .views import SearchProductView

urlpatterns = [
    url(r'^$', SearchProductView.as_view(), name='query'),
]

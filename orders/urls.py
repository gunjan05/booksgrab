from django.conf.urls import url

from .views import (
        OrderListView,
        OrderDetailView,
        GeneratePdf
        )

urlpatterns = [
    url(r'^$', OrderListView.as_view(), name='list'),
    url(r'^(?P<order_id>[0-9A-Za-z]+)/$', OrderDetailView.as_view(), name='detail'),
    url(r'^(?P<order_id>[0-9A-Za-z]+)/pdf/', GeneratePdf.as_view(), name='generatepdf'),
]

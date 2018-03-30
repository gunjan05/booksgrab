from django.conf.urls import url

from .views import (
        ProductListView,
        ProductDetailSlugView,
        ProductCFAListView,
        ProductERPListView,
        ProductCAIAListView,
        ProductFRMListView,
        ProductOthersListView
        )

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^cfa/', ProductCFAListView.as_view(), name='cfa'),
    url(r'^erp/', ProductERPListView.as_view(), name='erp'),
    url(r'^frm/', ProductFRMListView.as_view(), name='frm'),
    url(r'^caia/', ProductCAIAListView.as_view(), name='caia'),
    url(r'^others/', ProductOthersListView.as_view(), name='others'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
]

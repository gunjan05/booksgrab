from django.shortcuts import render
from django.db import models
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import ListView, DetailView, View
from .models import Order
from .utils import render_to_pdf
from billing.models import BillingProfile

class OrderListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):
    def get_object(self):
        request = self.request
        qs = Order.objects.by_request(
                    self.request
                ).filter(
                    order_id = self.kwargs.get('order_id')
                )

        if qs.count() == 1:
            return qs.first()

        raise Http404

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        obj = Order.objects.by_request(
                        self.request
                    ).filter(
                        order_id = self.kwargs.get('order_id')
                    )
        order_id = obj.first().order_id
        customer_name = obj.first().shipping_address.fullname
        # print(obj.first().billing_profile.user.mobile_number)
        order_date = obj.first().timestamp
        customer_address = obj.first().shipping_address.get_address()
        items = obj.first().cart
        from_address = 'ABC 123 Bhendi Bazar'
        data = {
            'order_id':order_id,
            'customer_name':customer_name,
            'order_date':order_date,
            'customer_address':customer_address,
            'items':items,
            'from_address':from_address,
        }

        pdf = render_to_pdf('orders/order_to_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

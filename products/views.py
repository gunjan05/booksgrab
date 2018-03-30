from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView, View
from .models import Product
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin
# Create your views here.

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/list.html'

    def get_context_data(self,*args,**kwargs):
        context = super(ProductListView, self).get_context_data(*args,**kwargs)
        cart_obj ,new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

class ProductCFAListView(ListView):
    template_name = 'products/list.html'

    def get_context_data(self,*args,**kwargs):
        context = super(ProductCFAListView, self).get_context_data(*args,**kwargs)
        cart_obj ,new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.cfa()

class ProductERPListView(ListView):
    template_name = 'products/list.html'

    def get_context_data(self,*args,**kwargs):
        context = super(ProductERPListView, self).get_context_data(*args,**kwargs)
        cart_obj ,new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.erp()

class ProductCAIAListView(ListView):
    template_name = 'products/list.html'

    def get_context_data(self,*args,**kwargs):
        context = super(ProductCAIAListView, self).get_context_data(*args,**kwargs)
        cart_obj ,new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.caia()

class ProductFRMListView(ListView):
    template_name = 'products/list.html'

    def get_context_data(self,*args,**kwargs):
        context = super(ProductFRMListView, self).get_context_data(*args,**kwargs)
        cart_obj ,new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.frm()

class ProductOthersListView(ListView):
    template_name = 'products/list.html'

    def get_context_data(self,*args,**kwargs):
        context = super(ProductOthersListView, self).get_context_data(*args,**kwargs)
        cart_obj ,new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.others()


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args,**kwargs)
        cart_obj ,new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404('Not Found')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404('Oops Something went Wrong!!')
        return instance

class ProductDetailView(ObjectViewedMixin, DetailView):
    # queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)

def product_detail_view(request, pk=None, *args, **kwargs):
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404('Product Doesnt exists')

    context = {'object':instance}
    return render(request,'products/detail.html', context)

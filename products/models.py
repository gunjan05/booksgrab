from decimal import Decimal
import random
import os
from django.urls import reverse
from django.db.models import Q
from django.db import models

from ecommerce.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

PRODUCT_CATEGORY_CHOICES=(
('cfa','CFA'),
('frm', 'FRM'),
('erp','ERP'),
('caia','CAIA'),
('others','Others'),
('free','Free')
)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext = os.path.splitext(base_name)
    return name,ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1000,9999)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename = new_filename , ext = ext)
    return 'products/{new_filename}/{final_filename}'.format(
                        new_filename = new_filename,
                        final_filename = final_filename
                        )

# class ProductQuerySet(models.query.QuerySet):
#     def cfa(self):
#         return self.filter(category='cfa')
#
#     def frm(self):
#         return self.filter(category='frm')
#
#     def erp(self):
#         return self.filter(category='erp')
#
#     def caia(self):
#         return self.filter(category='caia')
#
#     def others(self):
#         return self.filter(category='others')

class ProductManager(models.Manager):
    def get_by_id(self ,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()
        return None

    def cfa(self):
        return self.filter(category='cfa')

    def frm(self):
        return self.filter(category='frm')

    def caia(self):
        return self.filter(category='caia')

    def erp(self):
        return self.filter(category='erp')

    def others(self):
        return self.filter(category='others')

    def search(self, query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query) | Q(tag__title__icontains=query)
        return self.get_queryset().filter(lookups).distinct()


class Product(models.Model):
    active            = models.BooleanField(default=True)
    title             = models.CharField(max_length = 64)
    description       = models.TextField()
    author            = models.CharField(max_length = 100, default='Author')
    short_description = models.CharField(max_length = 100, default='A Short Description Of the Book')
    category          = models.CharField(max_length = 10, default = 'others', choices=PRODUCT_CATEGORY_CHOICES)
    price             = models.DecimalField(max_digits = 10, decimal_places = 2, default = 2000.00)
    display_price     = models.DecimalField(max_digits = 10, decimal_places = 2, default = 2000.00)
    percent_discount  = models.DecimalField(max_digits = 4, decimal_places = 2, default = 0.00)
    in_stock          = models.BooleanField(default=True)
    specs_line_1      = models.CharField(max_length = 150, default='Line 1', null=True, blank=True)
    specs_line_2      = models.CharField(max_length = 150, default='Line 2', null=True, blank=True)
    specs_line_3      = models.CharField(max_length = 150, default='Line 3', null=True, blank=True)
    specs_line_4      = models.CharField(max_length = 150, default='Line 4', null=True, blank=True)
    specs_line_5      = models.CharField(max_length = 150, default='Line 5', null=True, blank=True)
    image             = models.ImageField(upload_to = upload_image_path,null =True, blank = True)
    image2            = models.ImageField(upload_to = upload_image_path,null =True, blank = True)
    image3            = models.ImageField(upload_to = upload_image_path,null =True, blank = True)
    image4            = models.ImageField(upload_to = upload_image_path,null =True, blank = True)
    image5            = models.ImageField(upload_to = upload_image_path,null =True, blank = True)
    slug              = models.SlugField(blank=True, unique=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug':self.slug})

    def __str__(self):
        return str(self.title)


def product_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    discount =  instance.display_price - instance.price
    instance.percent_discount = (Decimal(discount)/Decimal(instance.display_price))*Decimal(100.00)

pre_save.connect(product_pre_save_reciever, sender = Product)

from django.db import models
from ecommerce.utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from products.models import Product
# Create your models here.
class Tag(models.Model):
    title             = models.CharField(max_length = 64)
    description       = models.TextField()
    author            = models.CharField(max_length = 20, default='Author')
    short_description = models.CharField(max_length = 20)
    price             = models.DecimalField(max_digits = 10, decimal_places = 2, default = 2000.00)
    slug              = models.SlugField()
    products          = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title


def tag_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_reciever, sender = Tag)

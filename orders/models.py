from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from carts.models import Cart
from billing.models import BillingProfile
from addresses.models import Address
from products.models import Product
from ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save ,post_save
import math
# Create your models here.
ORDER_STATUS_CHOICES = (
    ('Created', 'Created'),
    ('Paid','Paid'),
    ('Pending', 'Pending'),
    ('Shipped','Shipped'),
    ('Cancelled', 'Cancelled'),
    ('Delivered', 'Delivered'),
    ('Refunded','Refunded'),
)


class OrderManagerQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by("-updated", "-timestamp")

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='Created')


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
        created=False
        qs = self.get_queryset().filter(billing_profile=billing_profile,cart=cart_obj, active=True, status='Created')
        if qs.count()==1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile,cart=cart_obj)
            created=True
        return obj, created


class Order(models.Model):
    billing_profile     = models.ForeignKey(BillingProfile, null=True, blank=True)
    order_id            = models.CharField(max_length=30, blank=True)
    shipping_address    = models.ForeignKey(Address, related_name='shipping_address', null=True, blank=True)
    cart                = models.ForeignKey(Cart)
    status              = models.CharField(max_length=20, default='Created', choices=ORDER_STATUS_CHOICES)
    shipping_total      = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total               = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    active              = models.BooleanField(default=True)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    courier_company     = models.CharField(max_length=100, blank=True, null=True)
    tracking_id         = models.CharField(max_length=100, blank=True, null=True)
    delivery_date       = models.DateField(blank=True, null=True)
    payment_status      = models.CharField(max_length=50, default='False',null=True, blank=True)
    payment_id          = models.CharField(max_length=50, default='1234567',null=True, blank=True)
    payment_response    = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    class Meta:
       ordering = ['-timestamp', '-updated']

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        # billing_address = self.billing_address
        total = self.total
        if billing_profile and shipping_address and total>0: #and billing_address
            return True
        return False

    def get_absolute_url(self):
        return reverse("orders:detail", kwargs={'order_id': self.order_id})

    def mark_paid(self):
        if self.check_done():
            self.status = 'Paid'
            self.save()
        return self.status

    def mark_Notpaid(self):
        if not self.check_done():
            self.status = 'Pending'
            self.save()
        return self.status

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total

    def get_status(self):
        if self.status == 'Paid':
            return 'Paid, Shipping Soon'
        if self.status == 'Delivered':
            return 'Delivered'
        if self.status == 'Created':
            return 'Created (InCart)'
        if self.status == 'Cancelled':
            return 'Cancelled'
        if self.status == 'Pending':
            return 'Pending'
        if self.status == 'Refunded':
            return 'Refunded'
        return 'Error'


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count()==1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)

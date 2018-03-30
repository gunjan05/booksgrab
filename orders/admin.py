import csv
from django.utils.encoding import smart_str
from django.contrib import admin
from django.http import HttpResponse
from .models import Order

#from addresses.models import Address

def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"Order ID"),
        smart_str(u"Customer Email"),
        smart_str(u"Status"),
        smart_str(u"Total"),
        smart_str(u"Cart Items"),
        smart_str(u"Courier Company"),
        smart_str(u"Tracking ID"),
        smart_str(u"Date/Time"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.order_id),
            smart_str(obj.billing_profile),
            smart_str(obj.status),
            smart_str(obj.total),
            smart_str(obj.cart),
            smart_str(obj.courier_company),
            smart_str(obj.tracking_id),
            smart_str(obj.timestamp),
        ])
    return response
export_csv.short_description = u"Export CSV"

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'billing_profile', 'shipping_address', 'status','total','cart', 'courier_company', 'tracking_id', 'timestamp']
    actions = [export_csv]
    list_filter = ('status','timestamp')
    search_fields = ('order_id',)

    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)

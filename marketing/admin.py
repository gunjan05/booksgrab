from django.contrib import admin
from .models import MarketingPreference
# Register your models here.

class MarketingPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscribed', 'updated']
    readonly_fields = ['mailchimp_subscribed', 'timestamp', 'updated']
    class Meta:
        model = MarketingPreference
        fields = ['user', 'subscribed', 'mailchimp_msg', 'mailchimp_subscribed', 'timestamp', 'updated']

admin.site.register(MarketingPreference, MarketingPreferenceAdmin)

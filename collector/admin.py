from django.contrib import admin
from .models import Provider, Country, Province, City, Offer

class GenericAdmin(admin.ModelAdmin):
    list_display = ('key', 'id', 'value', 'order')
    list_filter = ('order',)
    
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'province', 'city', 'salary_max', 'salary_min')
    list_filter = ('country', 'province', 'city')

admin.site.register(Provider, GenericAdmin)
admin.site.register(Country, GenericAdmin)
admin.site.register(Province, GenericAdmin)
admin.site.register(City, GenericAdmin)
admin.site.register(Offer, OfferAdmin)
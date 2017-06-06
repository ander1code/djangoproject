from .models import *
from django.contrib import admin

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['nome']

class CarAdmin(admin.ModelAdmin):
    search_fields = ['plate']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Car, CarAdmin)



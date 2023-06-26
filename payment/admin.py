from django.contrib import admin
from .models import *


# Register your models here.


class OrderItemAdmin(admin.TabularInline):
    model = OrderItems


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid', 'is_sent', 'get_jalali_date', 'tracking_code')
    list_filter = ('is_paid', 'is_sent')
    inlines = (OrderItemAdmin,)
    search_fields = ('tracking_code',)

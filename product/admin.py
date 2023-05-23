from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price')
    list_filter = ('created_at',)
    search_fields = ('title', 'price')

    fieldsets = [
        ("نام و دسته بندی محصول",
         {
             'fields': ('title', 'id'),
         }),
        ('مشخصات محصول',
         {
             'fields': ('price', 'discount', 'weight', 'description', 'country', 'image')
         }),
        ('مشخصات بیشتر',
         {
             'classes': ('collapse', 'open'),
             'fields': ['battery_capacity', 'maximum_torque',
                        'speed_range', 'speed_gear', 'dimensions', 'hammer_mode',
                        'hit_per_minute', 'chuck_capacity', 'left_right_movement',
                        'has_battery', 'spare_battery', 'has_box',]
         }),
    ]

from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price')
    list_filter = ('created_at',)
    search_fields = ('title', 'price')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = [
        ("نام و دسته بندی محصول",
         {
             'fields': ('title',),
         }),
        ('مشخصات محصول',
         {
             'fields': ('price', 'discount', 'weight')
         }),
        ('توضیحات و تصویر محصول',
         {
             'classes': ('collapse', 'open'),
             'fields': ['description', 'image', 'power_battery', 'maximum_torque',
                        'speed_range', 'speed_gear', 'dimensions', 'hammer_mode', 'spare_battery', 'box',
                        'slug',]

         }),
    ]

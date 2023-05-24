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
             'fields': ('title', 'category', 'id'),
         }),
        ('مشخصات محصول',
         {
             'fields': ('price', 'post_price', 'discount', 'weight', 'description', 'country', 'image')
         }),
        ('مشخصات بیشتر',
         {
             'classes': ('collapse', 'open'),
             'fields': ['battery_capacity', 'maximum_torque',
                        'speed_range', 'speed_gear', 'dimensions', 'hammer_mode',
                        'hit_per_minute', 'chuck_capacity', 'left_right_movement',
                        'has_battery', 'spare_battery', 'has_box', 'additional_items']
         }),
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Image)
admin.site.register(AdditionalItems)

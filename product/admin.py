from django.contrib import admin
from .models import *


class SpecAdmin(admin.StackedInline):
    model = Spec


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price')
    list_filter = ('created_at',)
    search_fields = ('title', 'price')
    inlines = [SpecAdmin]

    fieldsets = [
        ("نام و دسته بندی محصول",
         {
             'fields': ('title', 'category', 'id'),
         }),
        ('مشخصات محصول',
         {
             'fields': ('price', 'discount', 'weight', 'description', 'image')
         }),
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


admin.site.register(Image)
admin.site.register(AdditionalItems)
admin.site.register(Spec)
admin.site.register(Favorite)

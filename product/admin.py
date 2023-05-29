from django.contrib import admin
from .models import *


class SpecAdmin(admin.StackedInline):
    model = Spec


class PictureAdmin(admin.TabularInline):
    model = Picture


class AdditionalItemAdmin(admin.TabularInline):
    model = AdditionalItems


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_price')
    list_filter = ('created_at',)
    search_fields = ('title', 'price')
    inlines = [PictureAdmin, SpecAdmin, AdditionalItemAdmin]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


admin.site.register(Favorite)

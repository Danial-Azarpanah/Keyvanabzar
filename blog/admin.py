from django.contrib import admin
from .models import Tag, Blog


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("show_image", "title", "get_jalali_date")
    search_fields = ("title", "text", "tag__title")
    list_filter = ("tag__title",)
    prepopulated_fields = {"slug": ("title",)}

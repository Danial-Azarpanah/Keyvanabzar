from django.contrib import admin
from .models import Category, Blog, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("show_image", "title", "get_jalali_date")
    search_fields = ("title", "text", "category__title")
    list_filter = ("category__title",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Comment)



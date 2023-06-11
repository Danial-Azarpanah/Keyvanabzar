from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import format_html, strip_tags
from persiantools.jdatetime import JalaliDate


class Tag(models.Model):
    title = models.CharField("عنوان", max_length=30)
    slug = models.SlugField("اسلاگ", unique=True, allow_unicode=True,
                            null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"


class Blog(models.Model):
    title = models.CharField("عنوان", max_length=30)
    slug = models.SlugField('اسلاگ', unique=True, null=True, blank=True, allow_unicode=True)
    text = RichTextUploadingField(verbose_name="متن")
    image = models.ImageField(upload_to="blogs/image/",
                              verbose_name="عکس اصلی")
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, verbose_name="تگ",
                                 null=True, blank=True)

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')
    get_jalali_date.short_description = "تاریخ ایجاد"

    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="60px" height="50px">')
    show_image.short_description = "تصویر"

    def short_content(self):
        return strip_tags(self.text)[:50] + '...'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-created_at"]


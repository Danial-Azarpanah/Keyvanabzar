from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import format_html, strip_tags
from mptt.models import MPTTModel
from persiantools.jdatetime import JalaliDate
from accounts.models import User


class Category(models.Model):
    title = models.CharField('عنوان دسته بندی', max_length=30)
    slug = models.SlugField('اسلاگ', allow_unicode=True, blank=True, null=True, unique=True)
    created_at = models.DateTimeField('تاریخ ایجاد دسته بندی', auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقالات'
        verbose_name_plural = 'دسته بندی‌ های مقالات'


class Blog(models.Model):
    title = models.CharField("عنوان", max_length=30)
    slug = models.SlugField('اسلاگ', unique=True, null=True, blank=True, allow_unicode=True)
    text = RichTextUploadingField(verbose_name="متن")
    image = models.ImageField(upload_to="blogs/image/",
                              verbose_name="عکس اصلی")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name="دسته بندی",
                                 on_delete=models.SET_NULL,
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


class Comment(models.Model):
    """
        Model to save user comments and replies
        """
    article = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comments',
                                verbose_name='مقاله مربوطه')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments', verbose_name='کاربر')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True,
                               verbose_name='کامنت پدر')
    body = models.TextField('متن کامنت')
    created_at = models.DateTimeField('تاریخ و زمان', auto_now_add=True)

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    def __str__(self):
        return f' نظر {self.body[:30]}  توسط کاربر  {self.user.phone_number}'

    class Meta:
        verbose_name = 'بازخورت مقاله'
        verbose_name_plural = 'بازخورد مقالات'

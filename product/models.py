from django.db import models
from persiantools.jdatetime import JalaliDate
from mptt.models import MPTTModel, TreeForeignKey
from accounts.models import *


# Create your models here.


class Category(MPTTModel):
    title = models.CharField('عنوان دسته بندی', max_length=30)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children',
                            verbose_name='زیردسته')
    slug = models.SlugField('اسلاگ', allow_unicode=True, blank=True, null=True, unique=True)
    created_at = models.DateTimeField('تاریخ ایجاد دسته بندی', auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی‌ ها'
        ordering = ['parent__id']


class AdditionalItems(models.Model):
    title = models.CharField('آیتم محصول', max_length=155)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'آیتم اضافی'
        verbose_name_plural = 'آیتم های اضافی'


class Image(models.Model):
    code = models.CharField("کد محصول", max_length=30, )
    image = models.ImageField('تصویر محصول', upload_to='products/')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصولات'


class Product(models.Model):
    id = models.CharField("کد محصول", max_length=30, unique=True, primary_key=True)
    title = models.CharField('عنوان محصول', max_length=100)
    image = models.ManyToManyField(Image, related_name='images',
                                   verbose_name='تصاویر محصول')
    category = models.ManyToManyField(Category, related_name='videos', verbose_name='دسته بندی')
    description = models.TextField('توضیحات محصول')
    price = models.PositiveIntegerField('قیمت(ریال)', default=0)
    post_price = models.PositiveIntegerField('هزینه ارسال', default=50)
    discount = models.PositiveIntegerField('درصد تخفیف', null=True, blank=True)
    battery_capacity = models.CharField('ظرفیت باتری', max_length=55, null=True, blank=True)
    maximum_torque = models.CharField('حداکثر گشتاور', max_length=55, null=True, blank=True)
    speed_range = models.CharField('بازه سرعتی', max_length=55, null=True, blank=True)
    speed_gear = models.CharField('تعداد دنده های سرعت', max_length=55, null=True, blank=True)
    weight = models.CharField('وزن', max_length=55)
    dimensions = models.CharField('ابعاد', max_length=55, null=True, blank=True)
    hammer_mode = models.BooleanField("حالت چکشی", default=False)
    hit_per_minute = models.IntegerField("ضربه در دقیقه", null=True, blank=True)
    chuck_capacity = models.IntegerField("ظرفیت سه نظام", null=True, blank=True)
    has_battery = models.BooleanField('باتری دارد', default=False)
    spare_battery = models.BooleanField('باتری یدک', default=False)
    left_right_movement = models.BooleanField('گردش چپ راست', default=False)
    has_box = models.BooleanField('جعبه دارد', default=False)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    country = models.CharField("کشور سازنده", max_length=30, null=True, blank=True)
    additional_items = models.ManyToManyField(AdditionalItems, related_name='items',
                                              verbose_name='آیتم اضافی', null=True, blank=True)

    def __str__(self):
        return F" محصول : {self.title} - {self.description[:30]}"

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('-created_at',)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites', verbose_name='محصول')

    def __str__(self):
        return f"{self.user.fullname} - {self.product.title}"

    class Meta:
        verbose_name = 'علاقه مندی'
        verbose_name_plural = 'علاقه مندی ها'

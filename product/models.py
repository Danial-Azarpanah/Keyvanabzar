from django.db import models
from persiantools.jdatetime import JalaliDate


# Create your models here.

class Product(models.Model):
    id = models.CharField("کد محصول", max_length=30, unique=True, primary_key=True)
    title = models.CharField('عنوان محصول', max_length=100)
    image = models.ImageField('تصویر محصول', upload_to='products/')
    description = models.TextField('توضیحات محصول')
    price = models.PositiveIntegerField('قیمت(ریال)', default=0)
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

    def __str__(self):
        return F" محصول : {self.title} - {self.description[:30]}"

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('-created_at',)

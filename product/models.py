from django.db import models
from persiantools.jdatetime import JalaliDate


# Create your models here.

class Product(models.Model):
    title = models.CharField('عنوان محصول', max_length=100)
    image = models.ImageField('تصویر محصول', upload_to='products/')
    description = models.TextField('توضیحات محصول')
    price = models.PositiveIntegerField('قیمت(ریال)', default=0)
    discount = models.PositiveIntegerField('درصد تخفیف', null=True, blank=True)
    power_battery = models.CharField('ظرفیت باتری', max_length=55)
    maximum_torque = models.CharField('حداکثر گشتاور', max_length=55)
    speed_range = models.CharField('بازه سرعتی', max_length=55)
    speed_gear = models.CharField('تعداد دنده های سرعت', max_length=55)
    weight = models.CharField('وزن', max_length=55)
    dimensions = models.CharField('ابعاد', max_length=55)
    hammer_mode = models.BooleanField("حالت چکشی")
    spare_battery = models.BooleanField('باتری یدک')
    box = models.BooleanField('جعبه')
    slug = models.SlugField("آدرس اسلاگ", unique=True, null=True, blank=True,
                            allow_unicode=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    def __str__(self):
        return F" محصول : {self.title} - {self.description[:30]}"

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('-created_at',)

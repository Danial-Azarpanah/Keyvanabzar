from mptt.models import MPTTModel, TreeForeignKey
from accounts.models import *
from django.db import models


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


class Product(models.Model):
    id = models.CharField("کد محصول", max_length=30, unique=True, primary_key=True)
    title = models.CharField('عنوان محصول', max_length=100)
    category = models.ManyToManyField(Category, related_name='categories', verbose_name='دسته بندی')
    country = models.CharField("کشور", max_length=50)
    description = models.TextField('توضیحات')
    price = models.PositiveIntegerField('قیمت (ریال)', default=0)
    discount = models.PositiveIntegerField('درصد تخفیف', null=True, blank=True)
    weight = models.CharField("وزن", max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return F" محصول : {self.id} - {self.title}"

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    def get_discounted_price(self):
        price = self.price - ((self.discount * 0.01) * self.price)
        return "{:,.0f} تومان ".format(price)

    def get_price(self):
        price = self.price
        return "{:,.0f} تومان ".format(price)

    get_price.short_description = 'قیمت'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('-created_at',)


class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField('تصویر محصول', upload_to='products/img/')

    def __str__(self):
        return self.picture.url

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصویر محصول'


class AdditionalItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    item = models.CharField('اقلام محصول', max_length=155)

    def __str__(self):
        return self.item

    class Meta:
        verbose_name_plural = 'اقلام همراه'
        verbose_name = 'اقلام محصول'


class Spec(models.Model):
    product = models.OneToOneField(Product,
                                   on_delete=models.CASCADE, related_name='specifications', verbose_name='محصول')

    battery_capacity = models.CharField("ظرفیت باتری (ولت)", max_length=30, null=True, blank=True)
    injection_force = models.CharField("نیروی تزریق (نیوتن)", max_length=30, null=True, blank=True)
    grease_capacity = models.CharField("ظرفیت گریس (گرم)", max_length=30, null=True, blank=True)
    hose_size = models.CharField("اندازه خرطوم (میلی متر)", max_length=30, null=True, blank=True)
    hit_rate = models.CharField("میزان ضربه (ضربه در دقیقه)", max_length=30, null=True, blank=True)
    chuck_size = models.CharField("اندازه سه نظام (میلی متر)", max_length=30, null=True, blank=True)
    surface_diameter = models.CharField("قطر صفحه (میلی متر)", max_length=30, null=True, blank=True)
    speed_range = models.CharField("بازه سرعتی (دور بر دقیقه)", max_length=30, null=True, blank=True)
    storage_capacity = models.CharField("ظرفیت مخزن (میلی لیتر)", max_length=30, null=True, blank=True)
    max_cut_depth = models.CharField("حداکثر عمق برش (میلی متر)", max_length=30, null=True, blank=True)
    maximum_torque = models.CharField("حداکثر گشتاور (نیوتن متر)", max_length=30, null=True, blank=True)
    injection_rate = models.CharField("نرخ تزریق (میلی متر بر دقیقه)", max_length=30, null=True, blank=True)
    injection_speed = models.CharField("سرعت تزریق (میلی متر بر دقیقه)", max_length=30, null=True, blank=True)
    tip_holder_size = models.CharField("اندازه نگهدارنده نوک (میلی متر)", max_length=30, null=True, blank=True)

    angle = models.CharField("زاویه (درجه)", max_length=30, null=True, blank=True)
    grease_type = models.CharField("نوع گریس", max_length=30, null=True, blank=True)
    gear_count = models.CharField("تعداد دور", max_length=30, null=True, blank=True)
    hit_force = models.CharField("قدرت ضربه (ژول)", max_length=30, null=True, blank=True)
    dimensions = models.CharField("ابعاد (میلی متر)", max_length=50, null=True, blank=True)
    input_watt = models.CharField("توان ورودی (وات)", max_length=30, null=True, blank=True)
    heat_range = models.CharField("بازه حرارتی (ولت)", max_length=30, null=True, blank=True)
    max_angle = models.CharField("حداکثر زاویه (درجه)", max_length=30, null=True, blank=True)
    working_modes = models.CharField("حالت‌های کار کردن", max_length=200, null=True, blank=True)
    base_size = models.CharField("اندازه پایه (میلی متر)", max_length=30, null=True, blank=True)
    colette_size = models.CharField("سایز کولت (میلی متر)", max_length=30, null=True, blank=True)
    rock_thickness = models.CharField("ضخامت سنگ (میلی متر)", max_length=30, null=True, blank=True)
    wind_force = models.CharField("قدرت پخش باد (کیلوگرم)", max_length=30, null=True, blank=True)
    blow_force = models.CharField("قدرت دمندگی (میلی متر)", max_length=30, null=True, blank=True)
    shake_rate = models.CharField("نرخ لرزش (لرزش بر دقیقه)", max_length=30, null=True, blank=True)
    grating_depth = models.CharField("عمق رنده کاری (میلی متر)", max_length=30, null=True, blank=True)
    cutting_angle_range = models.CharField("بازه زاویه برش (درجه)", max_length=30, null=True, blank=True)
    grating_rate = models.CharField("نرخ رنده کاری (متر بر دقیقه)", max_length=30, null=True, blank=True)

    sandpaper_dimensions = models.CharField("ابعاد سنباده (میلی متر)", max_length=30, null=True, blank=True)
    max_surface_diameter = models.CharField("حداکثر قطر صفحه (میلی متر)", max_length=30, null=True, blank=True)
    working_table_dimensions = models.CharField("ابعاد میز کار (میلی متر)", max_length=30, null=True, blank=True)
    max_hole_water = models.CharField("حداکثر قطر سوراخکاری با آب (میلی متر)", max_length=30, null=True, blank=True)
    sanding_circuit_length = models.CharField("طول مدار سنباده زنی (میلی متر)", max_length=30, null=True, blank=True)
    max_work_tool_dimensions = models.CharField("حداکثر قطر قطعه کار (میلی متر)", max_length=30, null=True, blank=True)
    max_cut_depth_wood = models.CharField("حداکثر عمق برش در چوب (میلی متر)", max_length=30, null=True, blank=True)
    max_cut_depth_iron = models.CharField("حداکثر عمق برش در آهن (میلی متر)", max_length=30, null=True, blank=True)
    vibration_rate = models.CharField("میزان ویبراسیون حین کار (m/s2)", max_length=30, null=True, blank=True)
    max_screw_diameter = models.CharField("حداکثر قطر پیچ (میلی متر)", max_length=30, null=True, blank=True)
    tool_holder_size = models.CharField("اندازه ابزارگیر (میلی متر)", max_length=30, null=True, blank=True)

    max_hole_not_water = models.CharField(
        "حداکثر قطر سوراخکاری بدون آب (میلی متر)", max_length=30, null=True, blank=True)
    max_45_90_angle = models.CharField(
        "حداکثر عمق برش در زوایای ۴۵ و ۹۰ (میلی متر)", max_length=30, null=True, blank=True)
    max_hole_diameter_wood_iron = models.CharField(
        "حداکثر قطر سوراخ در چوب و آهن (میلی متر)", max_length=30, null=True, blank=True)
    max_hole_cutting_tool = models.CharField(
        "حداکثر قطر سوراخکاری با ابزار برش (میلی متر)", max_length=30, null=True, blank=True)
    max_hole_diameter_wood_concrete = models.CharField("حداکثر قطر سوراخ در بتن (میلی متر)"
                                                       , max_length=30, null=True, blank=True)
    max_depth_cutting_tool = models.CharField(
        "حداکثر عمق سوراخکاری با ابزار برش (میلی متر)", max_length=30, null=True, blank=True)
    force_to_hole = models.CharField("میزان نیروی وارده به محل سوراخکاری (کیلوگرم)"
                                     , max_length=30, null=True, blank=True)

    has_box = models.BooleanField("جعبه دارد", default=False)
    has_dimmer = models.BooleanField("دیمر دار", default=False)
    has_hammer_mode = models.BooleanField("حالت چکشی", default=False)
    has_spare_battery = models.BooleanField("باتری یدک", default=False)
    has_safe_start = models.BooleanField("شروع ایمن دارد", default=False)
    is_brushless_mototr = models.BooleanField("سیستم بدون ذغال", default=False)
    has_left_right_movement = models.BooleanField("گردش چپ راست", default=False)
    excessive_watt_protection = models.BooleanField("محافظ اضافه بار", default=False)

    class Meta:
        verbose_name = 'مشخصه فنی'
        verbose_name_plural = 'مشخصات فنی'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites', verbose_name='محصول')

    def __str__(self):
        return f"{self.user.fullname} - {self.product.title}"

    class Meta:
        verbose_name = 'علاقه مندی'
        verbose_name_plural = 'علاقه مندی ها'


class DiscountCode(models.Model):
    name = models.CharField('نام کد تخفیف', max_length=30, )
    percent = models.PositiveIntegerField('درصد', default=0)
    quantity = models.PositiveIntegerField('تعداد', default=1)
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.quantity}'

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'

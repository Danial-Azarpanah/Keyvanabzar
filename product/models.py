from django.utils.html import format_html
from mptt.models import MPTTModel, TreeForeignKey
from accounts.models import *
from django.db import models


# Create your models here.


class Category(MPTTModel):
    title = models.CharField('عنوان دسته بندی', max_length=30)
    image = models.ImageField("تصویر دسته بندی", upload_to="categories/img/",
                              null=True, blank=True)
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
    category = models.ForeignKey(Category, related_name='categories', verbose_name='دسته بندی',
                                 on_delete=models.CASCADE, null=True, blank=True)
    proper_tools = models.ManyToManyField("self", related_name="proper_tools",
                                          verbose_name="ابزارهای مناسب", null=True, blank=True)
    country = models.CharField("کشور مونتاژ کننده", max_length=50)
    description = models.TextField('توضیحات')
    call_before = models.BooleanField("تماس قبل از خرید", default=False)
    price = models.PositiveIntegerField('قیمت (تومان)', default=0)
    discount = models.PositiveIntegerField('درصد تخفیف', null=True, blank=True)
    discounted_price = models.PositiveIntegerField('قیمت تخفیف خورده (تومان)', null=True, blank=True)
    weight = models.CharField("وزن", max_length=30)
    total_weight = models.FloatField("وزن همراه جعبه (کیلوگرم)", null=True, blank=True)
    created_at = models.DateTimeField("تاریخ قرارگیری در سایت", auto_now_add=True)
    sale_count = models.IntegerField("تعداد فروش", default=0)

    def __str__(self):
        return F" محصول : {self.id} - {self.title}"

    # Discount related processes
    def save(self, *args, **kwargs):
        discount, discounted_price = None, None

        try:
            discounted_price = self.price - (self.price * self.discount / 100)
            print(discounted_price, 1)
        except:
            pass

        try:
            discount = ((self.price - self.discounted_price) / self.price) * 100
            print(discount, 2)
        except:
            pass

        if discounted_price and discount:
            self.discounted_price = discounted_price
        elif discounted_price and not discount:
            self.discounted_price = discounted_price
            self.discount = self.discount
        elif discount and not discounted_price:
            self.discount = discount
            self.discounted_price = self.discounted_price
        else:
            self.discounted_price = self.price

        super().save(*args, **kwargs)

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    def get_discounted_price(self):
        price = self.discounted_price
        return "{:,.0f} تومان ".format(price)

    def get_discounted_price_admin(self):
        if self.discount and self.discount > 0:
            return self.get_discounted_price()
        return "-"

    get_discounted_price_admin.short_description = "قیمت تخفیف خورده"

    def get_price(self):
        price = self.price
        return "{:,.0f} تومان ".format(price)

    get_price.short_description = 'قیمت'

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ('discount',)


class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField('تصویر محصول', upload_to='products/img/')

    def __str__(self):
        return self.picture.url

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصویر محصول'


class AdditionalItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_items')
    item = models.CharField('اقلام محصول', max_length=155)

    def __str__(self):
        return self.item

    class Meta:
        verbose_name_plural = 'اقلام همراه'
        verbose_name = 'اقلام محصول'


class Spec(models.Model):
    title = models.CharField('مشخصه', max_length=255, null=True, blank=True)
    value = models.CharField('مقدار مشخصه', max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE, related_name='specifications', verbose_name='محصول')

    def __str__(self):
        return self.title

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


class Comparison(models.Model):
    """
    Model to save the products user wants to compare
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="comparison", verbose_name="کاربر")
    product1 = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                 related_name="productcompare1", verbose_name="کالای اول",
                                 null=True, blank=True)
    product2 = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                 related_name="productcompare2", verbose_name="کالای دوم",
                                 null=True, blank=True)

    def __str__(self):
        return self.user.fullname


class Comment(models.Model):
    """
    Model to save user comments and replies
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name='محصول مربوطه')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True,
                               verbose_name='کامنت پدر')
    body = models.TextField('متن کامنت')
    created_at = models.DateTimeField('تاریخ و زمان', auto_now_add=True)

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    def __str__(self):
        return f' نظر {self.body[:30]}  توسط کاربر  {self.user.phone_number}'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'


class DiscountCode(models.Model):
    name = models.CharField('نام کد تخفیف', max_length=30, )
    percent = models.PositiveIntegerField('درصد', default=0)
    quantity = models.PositiveIntegerField('تعداد', default=1)
    used_by = models.ManyToManyField(User, null=True, blank=True,
                                     verbose_name="استفاده شده توسط",
                                     related_name="discounts")
    expiration = models.DateTimeField('تاریخ انقضا', null=True, blank=True)

    def is_not_expired(self):
        if self.expiration >= timezone.localtime(timezone.now()):
            return True
        else:
            return False

    def __str__(self):
        return f'{self.name} - {self.quantity}'

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'


class Slider(models.Model):
    title = models.CharField("عنوان", max_length=20)
    text = models.CharField("توضیح کوتاه", max_length=30)
    image = models.ImageField("عکس اسلایدر (۱۹۲۰ * ۵۰۰)", upload_to="sliders/images/")
    url = models.URLField("آدرس برای هدایت کاربر", null=True)
    button_text = models.CharField("متن دکمه آدرس", max_length=20, default="اکنون خرید کنید")

    def __str__(self):
        return self.title

    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="60px" height="50px">')

    show_image.short_description = "عکس اسلایدر"

    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدرها"

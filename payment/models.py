from ghasedakpack import ghasedakpack

from accounts.models import *
from product.models import *


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    is_paid = models.BooleanField('پرداخت', default=False)
    is_sent = models.BooleanField("ارسال شده", default=False)
    total_price = models.PositiveIntegerField('قیمت کل')
    post_price = models.PositiveIntegerField("قیمت پست", null=True, blank=True)
    created_at = models.DateTimeField('تاریخ ثبت سفارش در', auto_now_add=True)
    tracking_code = models.IntegerField('کد رهگیری', editable=False)
    post_tracking_code = models.CharField("کد رهگیری پست", null=True, blank=True,
                                          max_length=100)
    discount_applied = models.BooleanField("تخفیف اعمال شده", default=False)
    address = models.TextField("آدرس", null=True, blank=True)
    delivery_method = models.CharField("نحوه ارسال", max_length=20,
                                       null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if self.is_sent:
    #         sms = ghasedakpack.Ghasedak("c24ff1b633a6e59dfdb9a5229be300bf1a122ca2fdf17ee3083a346b3d8864e6")
    #         sms.send({'message': 'این پیام جنبه تستی دارد', 'receptor': f'{self.user.phone_number}',
    #                   'linenumber': '10008566'})
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}'

    def get_post_price(self):
        return "{:,.0f} تومان ".format(self.post_price)

    def get_total_price(self):
        return "{:,.0f} تومان ".format(self.total_price)

    def get_post_and_total_price(self):
        return "{:,.0f} تومان ".format(self.total_price + self.post_price)

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    get_jalali_date.short_description = "تاریخ ثبت سفارش در"

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ('-created_at',)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name='محصول')
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField('قیمت')

    def get_price(self):
        return "{:,.0f} تومان ".format(self.price)

    def get_product_total(self):
        price = self.price * self.quantity
        return "{:,.0f} تومان ".format(price)

    def __str__(self):
        return f'{self.order} - - - {self.product.title}'

    class Meta:
        verbose_name = 'جزئیات سفارش'
        verbose_name_plural = 'جزئیات سفارش'

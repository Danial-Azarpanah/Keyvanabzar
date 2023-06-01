from accounts.models import *
from product.models import *


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
    is_paid = models.BooleanField('پرداخت', default=False)
    total_price = models.PositiveIntegerField('قیمت کل')
    created_at = models.DateTimeField('تاریخ ثبت سفارش در', auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        return "{:,.0f} تومان ".format(self.total_price)

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    get_jalali_date.short_description = "تاریخ ثبت سفارش در"

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'
        ordering = ('-created_at',)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name='محصول')
    price = models.PositiveIntegerField('قیمت')

    def __str__(self):
        return f'{self.order} - - - {self.product.title}'

    class Meta:
        verbose_name = 'جزئیات سفارش'
        verbose_name_plural = 'جزئیات سفارش'

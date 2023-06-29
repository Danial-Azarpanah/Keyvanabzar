from django.db import models
from django.utils import timezone
from persiantools.jdatetime import JalaliDate

from accounts.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    phone_number = models.CharField("شماره موبایل", max_length=11, unique=True)
    fullname = models.CharField('نام و نام خوانوادگی', max_length=100)
    date_joined = models.DateTimeField("تاریخ عضویت", auto_now_add=True)

    is_active = models.BooleanField('وضعیت کاربر', default=True)
    is_admin = models.BooleanField('مدیر', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['fullname']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.phone_number}"

    def get_jalali_date(self):
        return JalaliDate(self.date_joined, locale=('fa')).strftime('%c')

    get_jalali_date.short_description = "تاریخ ثبت نام در"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Otp(models.Model):
    token = models.CharField('توکن اعتبارسنجی', max_length=155, null=True)
    phone_number = models.CharField('شماره موبایل', max_length=11)
    fullname = models.CharField('نام و نام خانوادگی', max_length=50, null=True, blank=True)
    password = models.CharField('گذرواژه', max_length=100, null=True)
    code = models.CharField(' کد فعالسازی', max_length=6)
    expiration = models.DateTimeField('تاریخ انقضا', null=True, blank=True)

    def __str__(self):
        return F" : شماره موبایل  {self.phone_number}"

    def is_not_expired(self):
        if self.expiration >= timezone.localtime(timezone.now()):
            return True
        else:
            return False

    class Meta:
        verbose_name_plural = "کدهای اعتبارسنجی"
        verbose_name = "کد اعتبارسنجی"


class EditedUser(Otp):
    new_phone_number = models.CharField("شماره موبایل جدید", max_length=11)

    class Meta:
        verbose_name = "کد تایید ویرایش پروفایل"
        verbose_name_plural = "کدهای تایید ویرایش پروفایل"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='کاربر')
    address = models.CharField('آدرس', max_length=300)
    postal_code = models.CharField('کد پستی', null=True, blank=True, max_length=20)
    fullname = models.CharField('نام و نام خانوادگی', max_length=55)
    phone_number = models.CharField('شماره تماس', max_length=11)
    email = models.EmailField('ایمیل', null=True, blank=True)

    def __str__(self):
        return f"{self.address}  - - - {self.user.fullname}"

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'


class Info(models.Model):
    phone_number = models.CharField('شماره موبایل', max_length=11)
    telephone = models.CharField('شماره تلفن ثابت', max_length=11)
    email = models.EmailField('ایمیل')
    address = models.CharField('آدرس مغازه', max_length=100)
    instagram = models.URLField('اینستاگرام', null=True, blank=True)
    youtube = models.URLField('یوتوب', null=True, blank=True)
    twitter = models.URLField("توییتر", null=True, blank=True)
    telegram = models.URLField("تلگرام", null=True, blank=True)

    class Meta:
        verbose_name = 'اطلاعات تماس'
        verbose_name_plural = 'اطلاعات تماس'


class ContactUs(models.Model):
    fullname = models.CharField('نام و نام خانوادگی', max_length=55)
    email = models.EmailField('ایمیل')
    subject = models.CharField('موضوع', max_length=100)
    message = models.TextField('پیغام', max_length=100)
    created_at = models.DateTimeField('تاریخ ارسال پیام در', auto_now_add=True)

    def __str__(self):
        return self.message[:30]

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

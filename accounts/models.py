from django.db import models
from django.utils import timezone

from accounts.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    phone_number = models.CharField("شماره موبایل", max_length=11, unique=True)
    fullname = models.CharField('نام و نام خوانوادگی', max_length=100)
    avatar = models.FileField(upload_to="users/profile", null=True,
                              blank=True, verbose_name='عکس پروفایل')
    address = models.TextField("آدرس", null=True, blank=True)
    postal_code = models.PositiveIntegerField("کد پستی", null=True, blank=True)
    date_joined = models.DateTimeField("تاریخ عضویت", default=timezone.now())

    is_active = models.BooleanField('وضعیت کاربر', default=True)
    is_admin = models.BooleanField('مدیر', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['fullname']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.fullname} - {self.phone_number}"

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
    fullname = models.CharField('نام و نام خانوادگی', max_length=50, null=True)
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

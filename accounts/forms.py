from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import *


def check_number(value):
    if value[:2] != "09" or len(value) < 11:
        raise ValidationError('یک شماره تماس معتبر وارد کنید', code='check_number')
    try:
        int(value)
    except:
        raise ValidationError('یک شماره تماس معتبر وارد کنید', code='check_number')


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار گذرواژه', widget=forms.PasswordInput)
    phone_number = forms.CharField(label='شماره موبایل', widget=forms.TextInput({'maxlength': 11}),
                                   validators=[check_number])

    class Meta:
        model = User
        fields = ('phone_number',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("گذرواژه مشابه نمیباشد")
        elif len(password1 and password2) < 8:
            raise ValidationError("طول گذرواژه باید حداقل ۸ کاراکتر باشد")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="برای تغییر گذرواژه <a href=\"../password/\">اینجا</a> کلیک کنید"
    )

    class Meta:
        model = User
        fields = ('password', 'phone_number', 'is_active', 'is_admin')


class SignInForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field'}))

    password = forms.CharField(
        widget=forms.PasswordInput({'class': 'input-field'}))


class SignUpForm(forms.ModelForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'maxlength': 11}),
        validators=[check_number])
    fullname = forms.CharField(
        widget=forms.TextInput({'class': 'input-field', 'maxlength': 50})
    )
    password = forms.CharField(
        widget=forms.PasswordInput({'class': 'input-field'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput({'class': 'input-field'}))

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError("گذرواژه‌ها یکسان نیستند! دوباره سعی نمائید")
        if len(password1) < 8:
            raise ValidationError("طول گذرواژه باید حداقل ۸ کاراکتر باشد!")

    class Meta:
        model = User
        fields = ['phone_number', 'fullname', 'password']


class CheckOtpForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': ' کد تایید را وارد نمایید ', 'maxlength': 6}))


class EditProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    fullname = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'maxlength': 11}
        ),
        validators=[check_number])
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            {"class": "input-field"}
        )
    )
    postal_code = forms.CharField(
        required=False,
        widget=forms.TextInput(
            {"class": "input-field"}
        )
    )

    class Meta:
        model = User
        fields = ['fullname', 'phone_number',
                  'address', 'postal_code']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            {'class': 'input-field'}))

    new_password = forms.CharField(
        widget=forms.PasswordInput(
            {'class': 'input-field'}))

    repeat_new_password = forms.CharField(
        widget=forms.PasswordInput(
            {'class': 'input-field'}))

    def clean(self):
        new_password = self.cleaned_data.get("new_password")
        repeat_new_password = self.cleaned_data.get("repeat_new_password")
        if new_password and repeat_new_password and new_password != repeat_new_password:
            raise ValidationError("رمز عبور مشابه نمیباشد")
        if len(new_password) < 8:
            raise ValidationError("طول گذرواژه باید حداقل ۸ کاراکتر باشد!")


class ResetPasswordForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            {'class': 'input-field', 'placeholder': ' شماره موبایل خود را برای بازیابی گذرواژه وارد نمایید ',
             'maxlength': 11}), validators=[check_number])

    def clean_phone_number(self):
        if not User.objects.filter(phone_number=self.cleaned_data.get('phone_number')):
            raise ValidationError('کاربری با این شماره موبایل در سایت وجود ندارد')
        return self.cleaned_data.get('phone_number')


class ResetPasswordOtpForm(CheckOtpForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            {'class': 'input-field'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            {'class': 'input-field'}))

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("گذرواژه‌ها یکسان نیستند! دوباره سعی نمائید")
        if len(password) < 8:
            raise ValidationError("طول گذرواژه باید حداقل ۸ کاراکتر باشد!")

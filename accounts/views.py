from random import randint
from django.views.generic import *
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages as msg
from django.contrib.auth import authenticate, login

from .forms import *
from .mixins import *
from uuid import uuid4
from .models import Otp
from accounts import messages


class SignInView(AuthenticatedMixin, FormView):
    """
    View for user login
    """
    template_name = 'accounts/sign-in.html'
    form_class = SignInForm

    def post(self, req, *args, **kwargs):
        form = self.form_class(req.POST)
        next_url = req.GET.get('return_to')
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['phone'], password=form.cleaned_data['password'])
            if user is not None:
                login(req, user)
                if next_url:
                    return redirect(next_url)
                return redirect('home:home')
            else:
                form.add_error('phone', messages.WRONG_PASSWORD_OR_PHONE)
        return render(req, self.template_name, {'form': form})


class SignUpView(AuthenticatedMixin, FormView):
    """
    View for user registration
    """
    template_name = 'accounts/sign-up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        token = uuid4().hex
        code = randint(10000, 99999)
        expiration = timezone.localtime(timezone.now()) + timezone.timedelta(minutes=15)
        Otp.objects.create(token=token, code=code, expiration=expiration,
                           phone_number=form.cleaned_data.get('phone_number'),
                           fullname=form.cleaned_data.get('fullname'),
                           password=form.cleaned_data.get('password'))
        print(code)

        # SMS.verification(
        #     {'receptor': form.cleaned_data["phone_number"], 'type': '1', 'templates': 'my-template', 'param1': code}
        # )

        return redirect(reverse_lazy('accounts:check-otp') + f'?token={token}')


class CheckOtpView(FormView):
    """
    View for authenticating Otp codes for registration process
    """
    template_name = 'accounts/check-otp.html'
    form_class = CheckOtpForm

    def form_valid(self, form):
        token = self.request.GET.get("token")
        otp = Otp.objects.get(token=token)
        if otp.is_not_expired():
            if form.cleaned_data.get("code") == otp.code:
                User.objects.create_user(phone_number=otp.phone_number, fullname=otp.fullname,
                                         password=otp.password)
                user = User.objects.get(phone_number=otp.phone_number)
                login(self.request, user)
                Otp.objects.filter(phone_number=user.phone_number).delete()
                return redirect("home:home")
            form.add_error("code", messages.WRONG_OTP_CODE)
            return render(self.request, self.template_name, {"form": form})
        otp.delete()
        form.add_error('code', messages.EXPIRES_OTP)
        return render(self.request, self.template_name, {"form": form})


class EditProfileView(RequiredLoginMixin, View):
    """
    View for modifying profile
    """
    form_class = EditProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, "accounts/edit-profile.html", context={"form": form})

    def post(self, req):
        form = self.form_class(req.POST, instance=req.user)
        user = req.user
        old_phone = req.user.phone_number
        if form.is_valid():
            cd = form.cleaned_data
            new_phone = cd.get("phone_number")
            code = randint(10000, 99999)
            print(code)
            expiration = timezone.localtime(timezone.now()) + timezone.timedelta(minutes=10)
            if new_phone != old_phone:
                form.save()
                user.phone_number = old_phone
                user.save()
                token = uuid4().hex
                EditedUser.objects.create(
                    token=token,
                    phone_number=user.phone_number,
                    new_phone_number=new_phone,
                    code=code,
                    expiration=expiration,
                )
                return redirect(
                    reverse_lazy("accounts:change-phone") + f"?token={token}"
                )
            form.save()
            return redirect('accounts:edit-profile')
        return render(req, "accounts/edit-profile.html", {'form': form})


class ChangePhoneView(RequiredLoginMixin, FormView):
    """
    View for authenticating otp code for
    phone number modifying process
    """
    template_name = 'accounts/check-otp.html'
    form_class = CheckOtpForm

    def form_valid(self, form):
        cd = form.cleaned_data
        token = self.request.GET.get("token")

        try:
            edited_user = EditedUser.objects.get(token=token, code=cd.get("code"))
        except:
            form.add_error("code", "کد وارد شده صحیح نمی‌باشد")
            return render(self.request, "accounts/check-otp.html", {"form": form})

        if edited_user.is_not_expired():
            user = User.objects.get(phone_number=edited_user.phone_number)
            user.phone_number = edited_user.new_phone_number
            user.save()
            edited_user.delete()
            msg.success(self.request, "اطلاعات حساب کاربری شما با موفقیت تغییر یافت")
            return redirect("accounts:edit-profile")
        else:
            edited_user.delete()
            form.add_error("code", "کد وارد شده منقضی می‌باشد")
            return render(self.request, "accounts/check-otp.html", {"form": form})


class ChangePasswordView(RequiredLoginMixin, FormView):
    template_name = 'accounts/change-password.html'
    form_class = ChangePasswordForm

    def form_valid(self, form):
        user = self.request.user
        if user.check_password(form.cleaned_data.get('old_password')):
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect('home:home')
        else:
            form.add_error('old_password', messages.WRONG_OLD_PASSWORD)
            return render(self.request, self.template_name, {'form': form})


class ResetPasswordView(FormView):
    template_name = 'accounts/reset-password.html'
    form_class = ResetPasswordForm

    def form_valid(self, form):
        token = uuid4().hex
        code = randint(10000, 99999)
        expiration = timezone.localtime(timezone.now()) + timezone.timedelta(minutes=15)
        Otp.objects.create(token=token, code=code, expiration=expiration,
                           phone_number=form.cleaned_data.get('phone_number'))
        print(code)

        # SMS.verification(
        #     {'receptor': form.cleaned_data["phone_number"], 'type': '1', 'templates': 'randecode', 'param1': code}
        # )

        return redirect(reverse_lazy('accounts:reset-password-otp') + f'?token={token}')


class ResetPasswordOtpView(FormView):
    template_name = 'accounts/reset-password-otp.html'
    form_class = ResetPasswordOtpForm

    def form_valid(self, form):
        token = self.request.GET.get("token")
        otp = Otp.objects.get(token=token)
        if otp.is_not_expired():
            if form.cleaned_data['code'] == otp.code:
                user = User.objects.get(phone_number=otp.phone_number)
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
                otp.delete()
                return redirect('home:home')
            form.add_error('code', messages.WRONG_OTP_CODE)
            return render(self.request, self.template_name, {"form": form})
        otp.delete()
        form.add_error('code', messages.EXPIRES_OTP)
        return render(self.request, self.template_name, {"form": form})

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordOtpView, self).get_context_data(**kwargs)
        token = self.request.GET.get("token")
        otp = Otp.objects.get(token=token)
        context["user"] = User.objects.get(phone_number=otp.phone_number)
        return context


class AddAddressView(FormView):
    template_name = 'accounts/add-address.html'
    form_class = AddressForm

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        next_url = self.request.GET.get('return_to')
        if form.is_valid():
            address = form.save(commit=False)
            address.user = self.request.user
            address.save()
            if next_url:
                return redirect(next_url)
        return render(self.request, self.template_name, {'form': form})


class ContactUsView(View):
    template_name = 'accounts/contact-us.html'

    def get(self, request):
        info = Info.objects.all()
        return render(self.request, self.template_name, {'info': info})

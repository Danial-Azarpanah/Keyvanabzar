from django.contrib.auth import authenticate, login
from django.views.generic import *
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import *
from .mixins import *
from uuid import uuid4
from .models import Otp
from random import randint
from accounts import messages


class SignInView(AuthenticatedMixin, FormView):
    template_name = 'accounts/login.html'
    form_class = SignInForm

    def post(self, req, *args, **kwargs):
        form = self.form_class(req.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['phone'], password=form.cleaned_data['password'])
            if user is not None:
                login(req, user)
                return redirect('home:home')
            else:
                form.add_error('phone', messages.WRONG_PASSWORD_OR_PHONE)
        return render(req, self.template_name, {'form': form})


class SignUpView(AuthenticatedMixin, FormView):
    template_name = 'accounts/register.html'
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


class PersonalInfoView(RequiredLoginMixin, View):
    template_name = ''

    def get(self, req):
        return render(req, self.template_name, {'instance': req.user})


class EditPersonalInfoView(RequiredLoginMixin, View):
    template_name = ''
    form_class = EditPersonalInfoForm

    def get(self, req):
        form = self.form_class(instance=req.user)
        return render(req, self.template_name, {"form": form})

    def post(self, req):
        form = self.form_class(req.POST, instance=req.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:personal-info')
        return render(req, self.template_name, {'form': form})


class ChangePasswordView(RequiredLoginMixin, FormView):
    template_name = ''
    form_class = ChangePasswordForm

    def form_valid(self, form):
        user = self.request.user
        if user.check_password(form.cleaned_data.get('old_password')):
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect('accounts:personal-info')
        else:
            form.add_error('old_password', messages.WRONG_OLD_PASSWORD)
            return render(self.request, self.template_name, {'form': form})


class ResetPasswordView(FormView):
    template_name = 'accounts/reset-password.html'
    form_class = ResetPasswordForm

    def form_valid(self, form):
        token = uuid4().hex
        code = randint(100000, 999999)
        expiration = timezone.localtime(timezone.now()) + timezone.timedelta(minutes=15)
        Otp.objects.create(token=token, code=code, expiration=expiration,
                           phone_number=form.cleaned_data.get('phone_number'))
        print(code)

        # SMS.verification(
        #     {'receptor': form.cleaned_data["phone_number"], 'type': '1', 'templates': 'randecode', 'param1': code}
        # )

        return redirect(reverse_lazy('accounts:reset-password-otp') + f'?token={token}')


class ResetPasswordOtpView(FormView):
    template_name = 'accounts/password-reset-otp.html'
    form_class = ResetPasswordOtpForm

    def form_valid(self, form):
        token = self.request.GET.get("token")
        otp = Otp.objects.get(token=token)
        if otp.is_not_expired():
            if form.cleaned_data['code'] == otp.code:
                user = User.objects.get(phone_number=otp.phone_number)
                user.set_password(form.cleaned_data.get('new_password'))
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

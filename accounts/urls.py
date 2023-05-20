from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('sign-in', SignInView.as_view(), name='sign-in'),
    path('sign-up', SignUpView.as_view(), name='sign-up'),
    path('log-out/', LogoutView.as_view(next_page='home:home'), name='log-out'),

    path('check-otp', CheckOtpView.as_view(), name='check-otp'),

    path('personal-info/', PersonalInfoView.as_view(), name='personal-info'),
    path('edit-personal-info/', EditPersonalInfoView.as_view(), name='edit-personal-info'),

    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('verify-code/', ResetPasswordOtpView.as_view(), name='reset-password-otp'),
]

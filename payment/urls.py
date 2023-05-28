from django.urls import path
from .views import *

app_name = 'payment'
urlpatterns = [
    path('cart-detail', CartDetailView.as_view(), name='cart-detail'),
    path('cart-add', CartAddView.as_view(), name='cart-add'),
]

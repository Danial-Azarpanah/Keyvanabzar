from django.urls import path
from .views import *

app_name = 'payment'
urlpatterns = [
    path('cart-detail', CartDetailView.as_view(), name='cart-detail'),

    path('cart-add/<int:pk>', CartAddView.as_view(), name='cart-add'),
    path('cart-del/<str:pk>', CartDeleteView.as_view(), name='cart-del'),

    path('order-creation', OrderCreationView.as_view(), name='order-creation'),
]

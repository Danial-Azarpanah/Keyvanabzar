from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('product-list/', views.ProductListView.as_view(), name='product-list')
]

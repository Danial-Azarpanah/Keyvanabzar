from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('product-list/', views.ProductListView.as_view(), name='product-list'),
    path('add-favorite/<int:pk>', views.AddFavoriteView.as_view(), name='add-favorite'),
    path('favorite-list/', views.FavoriteListView.as_view(), name='favorite-list'),
]

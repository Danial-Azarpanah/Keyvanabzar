from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('product-list/', views.ProductListView.as_view(), name='product-list'),
    path('product/<str:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-favorite/<str:pk>', views.AddFavoriteView.as_view(), name='add-favorite'),
    path('favorite-list/', views.FavoriteListView.as_view(), name='favorite-list'),

    path('search/', views.SearchView.as_view(), name='search'),
]

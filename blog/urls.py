from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("blog-list", views.BlogListView.as_view(), name="list"),
    path("blog/<str:slug>", views.BlogDetailView.as_view(), name="detail"),
]
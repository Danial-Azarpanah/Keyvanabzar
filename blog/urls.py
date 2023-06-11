from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("blog-list", views.BlogListView.as_view(), name="list"),
]
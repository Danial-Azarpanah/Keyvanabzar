from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")),
    path('', include("accounts.urls")),
    path('', include("product.urls")),
    path('', include("payment.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

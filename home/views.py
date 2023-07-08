from django.db.models import Q
from django.views.generic import *

from blog.models import Blog
from product.models import *


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_categories"] = Category.objects.exclude(image="")[:10]
        context["most_selling_products"] = Product.objects.order_by("-sale_count")[:10]
        context["most_recent_products"] = Product.objects.order_by("-created_at")[:10]
        context["discounted_products"] = Product.objects.filter(discount__isnull=False, discount__gt=0)[:10]
        context["cheapest_products"] = Product.objects.order_by("discounted_price")[:10]
        context["cheapest_products"] = Product.objects.order_by("discounted_price")[:10]
        context["articles"] = Blog.objects.all()[:6]
        context["sliders"] = Slider.objects.all()
        return context

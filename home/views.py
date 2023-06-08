from django.db.models import Q
from django.views.generic import *
from product.models import *


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(image__isnull=False, parent__isnull=True)
        return context

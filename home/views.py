from django.shortcuts import render
from django.views.generic import *


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ...
        return context

from django.shortcuts import render
from django.views.generic import *
from .cart import Cart


# Create your views here.


class CartDetailView(View):
    template_name = 'payment/cart-detail.html'

    def get(self, request):
        return render(request, self.template_name, {})


class CartAddView(View):

    def get(self, request, pk):
        pass

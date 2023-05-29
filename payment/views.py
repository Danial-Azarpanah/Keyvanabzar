from product.models import Product
from django.views.generic import *
from django.shortcuts import *
from .cart import Cart


# Create your views here.


class CartDetailView(View):
    template_name = 'payment/cart-detail.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart})


class CartAddView(View):

    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        cart = Cart(request)
        cart.add(product)
        return redirect('payment:cart-detail')


class CartDeleteView(View):
    def get(self, request, pk):
        cart = Cart(request)
        cart.delete(pk)
        return redirect('payment:cart-detail')

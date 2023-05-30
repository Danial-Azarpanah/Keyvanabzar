from product.models import Product
from django.views.generic import *
from django.shortcuts import *
from .cart import Cart
from .models import *


# Create your views here.


class CartDetailView(View):
    template_name = 'payment/cart-detail.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart})


class CartAddView(View):

    def post(self, request, pk):
        product = Product.objects.get(id=pk)
        quantity = request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product, quantity)
        return redirect('payment:cart-detail')


class CartDeleteView(View):
    def get(self, request, pk):
        cart = Cart(request)
        cart.delete(pk)
        return redirect('payment:cart-detail')


class OrderCreationView(View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            OrderItems.objects.create(order=order, product=item['product'], price=item['price'])
        cart.del_cart()
        return redirect('payment:cart-detail')

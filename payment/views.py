from django.contrib import messages
from django.views.generic import *
from django.shortcuts import *
from .cart import Cart
from .models import *
from .messages import *


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
        return redirect('payment:order-detail', order.id)


class OrderDetailView(DetailView):
    template_name = 'payment/order-detail.html'
    model = Order


class ApplyDiscountCodeView(View):
    def post(self, request, pk):
        code = request.POST.get('discount_code')
        order = get_object_or_404(Order, id=pk)
        discount_code = get_object_or_404(DiscountCode, name=code)
        if discount_code.quantity == 0:
            messages.error(request, CODE_NOT_EXISTS, 'danger')
            return redirect('payment:order-detail', order.id)

        # Apply discount code process
        order.total_price -= order.total_price * discount_code.percent / 100
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        messages.error(request, f' کد تخفیف {discount_code.percent} درصدی با موفقیت روی سفارش شما اعمال شد ')
        return redirect('payment:order-detail', order.id)

from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import *
from django.shortcuts import *
from random import randint
from .messages import *
from .cart import Cart
from .models import *
import requests
import json


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
        tracking_code = randint(100000, 999999)
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total(), tracking_code=tracking_code)
        for item in cart:
            OrderItems.objects.create(order=order, product=item['product'], quantity=item['quantity'], price=item['price'])
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
        if not Order.objects.filter(user=request.user, discount_applied=True):
            if discount_code.is_not_expired():
                if discount_code.quantity == 0:
                    return JsonResponse({'error': CODE_NOT_EXISTS})

                # Apply discount code process
                order.total_price -= order.total_price * discount_code.percent / 100
                order.discount_applied = True
                for item in order.items.all():
                    item.price -= item.price * discount_code.percent / 100
                    item.save()
                order.save()
                discount_code.quantity -= 1
                discount_code.save()
                return JsonResponse(
                    {'success': f' کد تخفیف {discount_code.percent} درصدی با موفقیت روی سفارش شما اعمال شد '})
            return JsonResponse({'error': CODE_EXPIRES})
        return JsonResponse({'error': CODE_ALREADY_USED})


# ZARIN PAL INFORMATION
MERCHANT = ""
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = "http://127.0.0.1:8000/payment/order/verify/"


class SendRequestView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        total_price = order.total_price * 10
        request.session['order_id'] = str(order.id)
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price,
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.phone_number}
        }
        req_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        req = requests.post(
            url=ZP_API_REQUEST,
            data=json.dumps(req_data),
            headers=req_header
        )
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class VerifyView(View):
    def get(self, request):
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        order_id = request.session['order_id']
        order = Order.objects.get(id=int(order_id))
        total_price = order.total_price * 10
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": total_price,
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.is_paid = True
                    order.save()
                    return render(request, '')
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(
                        req.json()['data']['message']
                    ))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return redirect('home:main')

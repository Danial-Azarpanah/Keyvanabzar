from product.models import Category
from accounts.models import Info
from payment.cart import Cart


def category_list(req):
    categories = Category.objects.all()
    return {'categories': categories}


def cart_info(req):
    return {'cart': Cart(req)}


def info(req):
    return {'info': Info.objects.last()}

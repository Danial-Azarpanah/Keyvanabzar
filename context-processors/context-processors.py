from product.models import Category, Favorite
from accounts.models import Info
from payment.cart import Cart


def category_list(req):
    categories = Category.objects.all()
    return {'categories': categories}


def cart_info(req):
    return {'cart': Cart(req)}


def info(req):
    return {'info': Info.objects.last()}


def favorites(req):
    if req.user.is_authenticated:
        return {'favorite_products': Favorite.objects.filter(user=req.user).values_list('product_id', flat=True)}
    return []

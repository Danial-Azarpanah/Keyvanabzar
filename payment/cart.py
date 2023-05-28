from product.models import Product

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product):
        pass

    def __iter__(self):
        pass

    def total(self):
        pass

    def remove(self, pk):
        pass

    def remove_cart(self):
        pass

    def save(self):
        self.session.modified = True

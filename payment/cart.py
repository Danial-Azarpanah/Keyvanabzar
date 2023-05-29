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
        product_id = product.id
        if product_id not in self.cart:
            self.cart[product_id] = {'id': product.id, 'title': product.title,
                                     'price': str(product.price), 'quantity': 1}
        self.save()

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            item['product'] = Product.objects.get(id=int(item['id']))
            item['total'] = int(item['quantity']) * int(item['price'])
            yield item

    def total(self):
        pass

    def delete(self, pk):
        if pk in self.cart:
            del self.cart[pk]
            self.save()

    def delete_cart(self):
        pass

    def save(self):
        self.session.modified = True

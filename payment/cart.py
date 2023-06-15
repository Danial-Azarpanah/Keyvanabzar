from product.models import Product

CART_SESSION_ID = 'cart'


def calculate_post_price(weight):
    if 0 < weight <= 1:
        return ["{:,.0f} تومان ".format(40000), 40000]
    return ["{:,.0f} تومان ".format(8000 * weight + 32000), 8000 * weight + 32000]


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity):
        product_id = product.id
        if product.discount:
            price = str(product.price - (int(product.discount * 0.01 * product.price)))
        else:
            price = product.price
        if product_id not in self.cart:
            self.cart[product_id] = {'id': str(product.id), 'title': product.title,
                                     'price': price,
                                     'formatted_price': "{:,.0f} تومان ".format(int(price)),
                                     'post_weight': 0,
                                     'quantity': 0}
        self.cart[product_id]['quantity'] += int(quantity)
        self.cart[product_id]['post_weight'] += int(quantity) * product.total_weight
        self.save()

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            item['product'] = Product.objects.get(id=item['id'])
            item['total'] = int(item['quantity']) * int(item['price'])
            item['formatted_total'] = "{:,.0f} تومان ".format(item['total'])
            yield item

    def total(self):
        cart = self.cart.values()
        total = 0
        for item in cart:
            total += int(item['quantity']) * int(item['price'])
        return total

    def get_post_price(self):
        cart = self.cart.values()
        total = 0
        for item in cart:
            total += item["post_weight"]
        if total > 30:
            return [0, 0]
        return calculate_post_price(total)

    def get_price(self, id):
        cart = self.cart.copy()
        return cart[id]["price"]

    def get_total(self):
        total = self.total()
        return "{:,.0f} تومان ".format(total)

    def get_total_and_post(self):
        total = self.total()
        post_price = self.get_post_price()
        return "{:,.0f} تومان ".format(total + post_price[1])

    def len(self):
        return len(self.cart)

    def delete(self, pk):
        if pk in self.cart:
            del self.cart[pk]
            self.save()

    def del_cart(self):
        del self.session[CART_SESSION_ID]

    def save(self):
        self.session.modified = True

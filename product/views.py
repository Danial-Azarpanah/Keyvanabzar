from django.views.generic import *
from django.shortcuts import *
from accounts.mixins import *
from product.models import *


# Create your views here.

class ProductListView(ListView):
    template_name = 'product/product-list.html'
    model = Product
    paginate_by = 10


class AddFavoriteView(View):
    def get(self, req, pk):
        try:
            fav = Favorite.objects.get(product_id=pk, user_id=req.user.id)
            fav.delete()
        except:
            Favorite.objects.create(product_id=pk, user_id=req.user.id)
        return redirect('product:favorite-list')


class FavoriteListView(RequiredLoginMixin, View):
    template_name = "product/favorite-list.html"

    def get(self, req, **kwargs):
        favorites = Product.objects.filter(favorites__user=req.user)
        return render(req, self.template_name, {"favorites": favorites})

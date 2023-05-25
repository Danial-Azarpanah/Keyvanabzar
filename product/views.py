from django.shortcuts import redirect
from django.views.generic import *
from product.models import *


# Create your views here.

class ProductListView(ListView):
    template_name = 'product/product-list.html'
    model = Product
    paginate_by = 10


class AddFavoriteView(View):
    def get(self, request, pk):
        try:
            fav = Favorite.objects.get(product_id=pk, user_id=request.user.id)
            fav.delete()
        except:
            Favorite.objects.create(product_id=pk, user_id=request.user.id)
        return redirect('home:home')

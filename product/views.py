from django.views.generic import *
from product.models import *


# Create your views here.

class ProductListView(ListView):
    template_name = 'product/product-list.html'
    model = Product
    paginate_by = 10

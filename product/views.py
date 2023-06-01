from django.views.generic import *
from django.shortcuts import *
from accounts.mixins import *
from product.models import *
from django.db.models import Q


# Create your views here.

class ProductListView(ListView):
    template_name = 'product/product-list.html'
    model = Product
    paginate_by = 24


class ProductDetailView(View):

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        spec_list = product.specifications
        comments = Comment.objects.filter(product=product)
        fields_with_values = []
        for field in spec_list._meta.fields[2:]:
            value = getattr(spec_list, field.name)
            if value:
                if value == True:
                    fields_with_values.append((field.verbose_name, "دارد"))
                else:
                    fields_with_values.append((field.verbose_name, value))
        print(fields_with_values)
        return render(request, "product/product-detail.html", {"product": product,
                                                               "specs": fields_with_values,
                                                               "comments": comments})

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("accounts:sign-in")

        product = get_object_or_404(Product, id=pk)
        parent = request.POST.get("parent-id")
        comment = request.POST.get("comment")

        Comment.objects.create(user=request.user, product=product, parent_id=parent, body=comment)
        return redirect(reverse("product:product-detail", kwargs={"pk": pk}))


class AddFavoriteView(RequiredLoginMixin, View):
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


class SearchView(ListView):
    template_name = 'product/search-result.html'
    model = Product
    paginate_by = 1

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Product.objects.filter(Q(title__icontains=q) | Q(id__icontains=q))

from product.models import *
from accounts.mixins import *
from django.shortcuts import *
from django.db.models import Q
from django.views.generic import *
from django.core.paginator import Paginator


class ProductListView(View):
    """
    View for showing all products
    """
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.all()

        # pagination
        page_number = request.GET.get('page')
        paginator = Paginator(products, 24)
        objects_list = paginator.get_page(page_number)

        context = {"products": objects_list, "categories": categories}
        return render(request, 'product/product-list.html', context)


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
    paginate_by = 24

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Product.objects.filter(Q(title__icontains=q) | Q(id__icontains=q))


class CategoryDetailView(View):
    """
    View for returning products
    based on their category
    """

    def get(self, request, pk):
        category = get_object_or_404(Category, slug=pk)
        products = Product.objects.filter(category__title=category)

        # pagination
        page_number = request.GET.get('page')
        paginator = Paginator(products, 24)
        objects_list = paginator.get_page(page_number)

        context = {"products": objects_list, "category": category}
        return render(request, 'product/category-detail.html', context)


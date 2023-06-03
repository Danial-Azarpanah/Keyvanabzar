from product.models import *
from accounts.mixins import *
from django.shortcuts import *
from django.views.generic import *
from django.core.paginator import Paginator
from django.db.models import Q, PositiveIntegerField, Case, When


class ProductListView(View):
    """
    View for showing all products
    """

    def get(self, request):
        categories = Category.objects.all()
        q = request.GET.get("q")
        if not q:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(Q(title__icontains=q) | Q(id__icontains=q))

        category = request.GET.get("category")
        filter = request.GET.get("filter")
        price_range = request.GET.get("price")

        if category:
            products = products.filter(category__slug=category)

        if price_range:
            price_range = price_range.replace("تومان", "").replace(" ", "").replace(",", "")
            min_price, max_price = price_range.split("-")
            products = products.filter((Q(price__gte=min_price) & Q(price__lte=max_price)) | (
                        Q(discounted_price__gte=min_price) & Q(discounted_price__lte=max_price)))

        if filter:
            if filter == "most-recent":
                products = products.order_by("-created_at")
            elif filter == "cheapest":
                products = products.annotate(
                    sorted_price=Case(
                        When(discounted_price__isnull=False, then='discounted_price'),
                        default='price',
                        output_field=PositiveIntegerField(),
                    )
                ).order_by('sorted_price')
            elif filter == "most-expensive":
                products = products.annotate(
                    sorted_price=Case(
                        When(discounted_price__isnull=False, then='discounted_price'),
                        default='price',
                        output_field=PositiveIntegerField(),
                    )
                ).order_by('-sorted_price')
            else:
                products = products.order_by("-sale_count")
        else:
            products = products.order_by("-sale_count")


        # pagination
        products_count = products.count()
        page_number = request.GET.get('page')
        paginator = Paginator(products, 1)
        objects_list = paginator.get_page(page_number)

        context = {"products": objects_list, "categories": categories,
                   "products_count": products_count}
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

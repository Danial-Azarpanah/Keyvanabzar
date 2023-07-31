from django.http import JsonResponse

from product.models import *
from accounts.mixins import *
from django.shortcuts import *
from django.views.generic import *
from django.contrib import messages as msg
from django.core.paginator import Paginator
from django.db.models import Q, PositiveIntegerField, Case, When

import csv
from django.http import HttpResponse


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
            products = products.filter(Q(category__slug=category) | Q(category__parent__slug=category))

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
        paginator = Paginator(products, 24)
        objects_list = paginator.get_page(page_number)

        context = {"products": objects_list, "categories": categories,
                   "products_count": products_count}
        return render(request, 'product/product-list.html', context)


class ProductDetailView(View):

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        comments = Comment.objects.filter(product=product)
        related_products = Product.objects.filter(category__title=product.category.title).exclude(title=product.title)
        return render(request, "product/product-detail.html", {"product": product,
                                                               "comments": comments,
                                                               "related_products": related_products})

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
            obj = Favorite.objects.get(product_id=pk, user_id=req.user.id)
            obj.delete()
            return JsonResponse({'response': 'deleted'})
        except:
            Favorite.objects.create(product_id=pk, user_id=req.user.id)
            return JsonResponse({'response': 'created'})


class RemoveFavoriteView(View):
    def get(self, req, pk):
        favorite_obj = Favorite.objects.get(product_id=pk)
        favorite_obj.delete()
        return redirect('product:favorite-list')


class AddCompareView(RequiredLoginMixin, View):
    """
    View for adding a product for comparison
    """

    def get(self, req, pk):
        product = Product.objects.get(id=pk)

        if Comparison.objects.filter(user=req.user).count() < 4:
            if Comparison.objects.filter(user=req.user, product=product).exists():
                return JsonResponse(
                    {'error': "نمی‌توانید دو کالای یکسان در سبد مقایسه خود داشته باشید"})
            elif Comparison.objects.filter(Q(user=req.user) & ~Q(product__category=product.category)).exists():
                return JsonResponse(
                    {'error': "کالای منتخب باید با کالای موجود در لیست مقایسه شما، دسته بندی یکسان داشته باشد"})
            else:
                obj = Comparison.objects.create(user=req.user, product=product)
                obj.save()
                return redirect(reverse("product:product-detail", kwargs={"pk": pk}))
        else:
            return JsonResponse(
                {"error": "نمی‌توانید بیشتر از ۴ کالا برای مقایسه انتخاب کنید"}
            )


class FavoriteListView(RequiredLoginMixin, View):
    template_name = "product/favorite-list.html"

    def get(self, req, **kwargs):
        favorites = Product.objects.filter(favorites__user=req.user)
        return render(req, self.template_name, {"favorites": favorites})


class CompareListView(RequiredLoginMixin, View):
    """
    View for showing the comparison list
    """

    def get(self, req):
        products = []
        fields = {}
        max_length = 0

        items = Comparison.objects.filter(user=req.user)
        for item in items:
            products.append(item.product)

        for i, product in enumerate(products):
            for spec in product.specifications.all():
                if spec.title in fields:
                    fields[f"{spec.title}"].append([i, spec.value])
                else:
                    fields[f"{spec.title}"] = [[i, spec.value]]
                    
        for i in fields.values():
            if len(i) > max_length:
                max_length = len(i)

        context = {"products": products, "fields": fields, "max_length": max_length}
        return render(req, "product/comparison-list.html", context)


class RemoveComparisonView(RequiredLoginMixin, View):
    """
    View for removing a product
    from the comparison list
    """

    def get(self, req, pk):
        comparison = Comparison.objects.get(user=req.user, product_id=pk)
        comparison.delete()

        return redirect("product:comparison-list")


def export_products_csv(request):
    if not request.user.is_authenticated:
        return redirect(
            reverse_lazy("accounts:sign-in") + f"?return_to=/get-csv"
        )
    if request.user.is_admin:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Price'])

        # Retrieve all products from the database
        products = Product.objects.all()

        # Iterate through each product and write its information to the CSV file
        for product in products:
            writer.writerow([product.id, product.get_csv_price()])

        return response

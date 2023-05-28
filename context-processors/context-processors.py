from product.models import Category


def category_list(req):
    categories = Category.objects.all()
    return {'categories': categories}

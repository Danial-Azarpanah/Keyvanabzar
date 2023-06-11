from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import View
from .models import Blog, Tag


class BlogListView(View):

    def get(self, request):
        articles = Blog.objects.all()
        page = request.GET.get("page")
        paginator = Paginator(articles, 1)
        object_list = paginator.get_page(page)

        tags = Tag.objects.all()
        return render(request, "blog/blog-list.html", {"articles": object_list,
                                                       "tags": tags})

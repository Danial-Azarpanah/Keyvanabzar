from django.db.models import Q
from django.urls import reverse
from django.views.generic import View
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .models import Blog, Comment, Category


class BlogListView(View):
    """
    View for returning blogs in a page
    """

    def get(self, request):
        articles = Blog.objects.all()
        comments = Comment.objects.filter(parent__isnull=True)[:5]

        s = request.GET.get("s")
        category = request.GET.get("category")
        if s:
            articles = articles.filter(Q(title__icontains=s) | Q(category__title__icontains=s))
        if category:
            articles = articles.filter(Q(category__slug=category))

        page = request.GET.get("page")
        paginator = Paginator(articles, 1)
        object_list = paginator.get_page(page)

        categories = Category.objects.all()
        articles = Blog.objects.all()[:5]
        return render(request, "blog/blog-list.html", {"articles": object_list,
                                                       "all_articles": articles,
                                                       "comments": comments,
                                                       "blog_categories": categories})


class BlogDetailView(View):
    """
    View for returning blog detail
    """

    def get(self, request, slug):
        article = get_object_or_404(Blog, slug=slug)
        articles = Blog.objects.all()[:5]
        categories = Category.objects.all()
        comments = Comment.objects.filter(parent__isnull=True)[:5]
        suggested_articles = Blog.objects.filter(category__title=article.category.title)[:3]
        return render(request, "blog/blog-detail.html", {"article": article,
                                                         "articles": articles,
                                                         "comments": comments,
                                                         "blog_categories": categories,
                                                         "suggested_articles": suggested_articles})

    def post(self, request, slug):
        if not request.user.is_authenticated:
            return redirect("accounts:sign-in")

        article = get_object_or_404(Blog, slug=slug)
        parent = request.POST.get("parent-id")
        comment = request.POST.get("comment")

        Comment.objects.create(user=request.user, article=article, parent_id=parent, body=comment)
        return redirect(reverse("blog:detail", kwargs={"slug": slug}))


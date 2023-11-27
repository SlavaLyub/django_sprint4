from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.constants import NUMBER_OF_POSTS
from blog.models import Category, Post


def index(request):
    template = 'blog/index.html'
    posts_index_list = Post.published.get_queryset().order_by(
        '-pub_date'
    )[:NUMBER_OF_POSTS]
    context = {'page_obj': posts_index_list}
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.published,
        pk=post_id,
    )
    context = {'post': post}
    template = 'blog/detail.html'
    return render(request, template, context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug,)

    post_list = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
    )

    context = {
        'category': category,
        'post_list': post_list,
    }
    template = 'blog/category.html'
    return render(request, template, context)

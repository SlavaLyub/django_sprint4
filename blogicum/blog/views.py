# from django.shortcuts import get_object_or_404, render
# from blog.constants import NUMBER_OF_POSTS
from blog.models import Post  # Category,
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

# from django.utils import timezone


class PostListView(ListView):
    """."""

    model = Post
    ordering = 'id'
    paginate_by = 10
    template_name = 'blog/index.html'


class PostDetailView(DetailView):
    """."""

    model = Post
    template_name = 'blog.detail.html'


class PostCreateView(CreateView):
    """."""

    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class PostUpdateView(UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    ...

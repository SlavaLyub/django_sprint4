# from blog.constants import NUMBER_OF_POSTS
from typing import Any

from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post, User  # Category,
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)


class PostListView(ListView):
    """Просмотр главной страницы."""

    model = Post
    ordering = ('-pub_date',)
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_queryset(self):
        return super().get_queryset().annotate(comment_count=Count('comments'))


class PostCreateView(LoginRequiredMixin, CreateView):
    """Класс создания поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        """Если форма заполнена валидно, сохранить в бд."""
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class PostDetailView(DetailView):
    """Просмотр отдельного поста."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'


    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        object = self.get_object()
        context['comments'] = object.comments.order_by('created_at')
        return context

    def get_queryset(self):
        if self.queryset is None:
            return self.model.objects.all()


class UserDetailView(DetailView):
    """Просмотр страницы пользователя."""

    model = User
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование поста."""

    model = Post
    fields = ('title', 'text', 'pub_date', 'location', 'category')
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self) -> str:
        """Переадресация после редактирования."""
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})

    def form_valid(self, form):
        """Если форма заполнена валидно, сохранить в бд."""
        if form.instance.author != self.request.user:
            return redirect(self.get_success_url())
        self.object = form.save()
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs: Any):
        """заполняется форма которую удаляем."""
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.get_object())  # еще раз обсудить как работает
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария."""

    model = Comment
    form_class = CommentForm
    # template_name = ''
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        """Если форма заполнена валидно, сохранить в бд."""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        self.object = form.save()
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование комментария."""

    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        """Если форма заполнена валидно, сохранить в бд."""
        if form.instance.post != get_object_or_404(Post, pk=self.kwargs['post_id']):
            raise Comment.DoesNotExist()
        if form.instance.author != self.request.user:
            raise PermissionDenied()
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Переадресация на страницу с публикацией."""
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление комментария."""

    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self) -> str:
        """Переадресация на страницу с публикацией."""
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})

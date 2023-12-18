from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import CommentForm, PostForm, UserForm
from blog.models import Category, Comment, Post, PostQuerySet, User
from .constants import PAGINATE_BY


class AuthorRequiredMixin():

    def dispatch(self, request, *args, **kwargs):
        if (request.user == self.get_object().author):
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class RelatedPostsViewMixin():
    model = Post

    def get_queryset(self):
        """Список постов автора или категории."""
        self.object = self.get_object()
        return PostQuerySet.add_comments(PostQuerySet.add_filter(
            self.get_user_id(), self.object.posts
        ))


class PostListView(ListView):
    """Просмотр главной страницы."""

    ordering = ('-pub_date',)
    paginate_by = PAGINATE_BY
    template_name = 'blog/index.html'

    def get_queryset(self):
        """Список постов автора."""
        return PostQuerySet.add_filter(
            None,
            PostQuerySet.add_comments(Post.objects)
        )


class PostCreateView(LoginRequiredMixin, CreateView):
    """Класс создания поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )

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

    def get_queryset(self):
        return PostQuerySet.add_filter(
            self.request.user.id,
            super().get_queryset()
        )

    def get_context_data(self, **kwargs):
        """Передача формы для написания комментария."""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments
            .select_related('author')
            .order_by('created_at')
        )
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование поста."""

    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self) -> str:
        """Переадресация после редактирования."""
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """Удаление поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        """заполняется форма которую удаляем."""
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.get_object())
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария."""

    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )

    def form_valid(self, form):
        """Если форма заполнена валидно, сохранить в бд."""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        self.object = form.save()
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Редактирование комментария."""

    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self) -> str:
        """Переадресация на страницу с публикацией."""
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """Удаление комментария."""

    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self) -> str:
        """Переадресация на страницу с публикацией."""
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Страница редактирования профиля."""

    model = User
    template_name = 'blog/user.html'
    form_class = UserForm
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        """Определил объект для класса."""
        return self.request.user


class UserDetailView(RelatedPostsViewMixin, ListView):
    """Просмотр страницы пользователя."""

    template_name = 'blog/profile.html'
    paginate_by = PAGINATE_BY

    def get_object(self):
        return get_object_or_404(
            User, username=self.kwargs['username']
        )

    def get_user_id(self):
        return self.request.user.id

    def get_context_data(self, **kwargs):
        """Получаем словарь контекста."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context


class CategoryDetailView(RelatedPostsViewMixin, LoginRequiredMixin, ListView):
    """Просмотр страницы категории."""

    template_name = 'blog/category.html'
    paginate_by = PAGINATE_BY

    def get_user_id(self):
        return None

    def get_object(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
        )

    def get_context_data(self, **kwargs):
        """Получаем словарь контекста."""
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context

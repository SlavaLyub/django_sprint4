from blog.constants import CHAR_LENGHT
from core.models import Base
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

User = get_user_model()


class PostQuerySet(models.QuerySet):
    """Менеджер модели Post."""

    def get_posts(self):
        """
        Запрос к БД фильтр по:
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True.
        """
        return self.select_related(
            'location',
            'category',
            'author',
        ).filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )


class PostManager(models.Manager):
    """Делает запрос к модели Post и связанным моделям Location, Category."""

    def get_queryset(self) -> QuerySet:
        return PostQuerySet(self.model).get_posts()


class Post(Base):
    author = models.ForeignKey( # manyToOne
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts')
    title = models.CharField(
        max_length=CHAR_LENGHT,
        verbose_name='Заголовок')
    text = models.TextField(
        verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.'))
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Местоположение',
        related_name='posts')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts')
    # comments = models.OneToMany('Comment', related_name='post')
    image = models.ImageField(null=True, blank=True, upload_to='posts')
    objects = models.Manager()
    published = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)


class Category (Base):
    title = models.CharField(
        max_length=CHAR_LENGHT,
        verbose_name='Заголовок')
    description = models.TextField(
        verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ))

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(Base):
    name = models.CharField(
        max_length=CHAR_LENGHT,
        verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='comments'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
        )
    text = models.TextField(
        verbose_name='Текст',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='публикация',
        related_name='comments'
    )

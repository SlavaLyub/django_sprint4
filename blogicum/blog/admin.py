from django.contrib import admin

from .constants import SHORT_STANDARD, SHORT_STANDARD_MIN
from .models import Category, Location, Post


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'is_published',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'created_at',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'is_published',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'short_title',
        'short_text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
    )
    list_editable = (
        'pub_date',
        'location',
        'category',
        'is_published',
    )
    list_filter = (
        'location',
        'category',
        'is_published',
    )
    ordering = (
        '-pub_date',
    )

    @admin.display(description='Заголовок')
    def short_title(self, obj):
        return obj.title[:SHORT_STANDARD]

    @admin.display(description='Текст')
    def short_text(self, obj):
        return obj.text[:SHORT_STANDARD]

    @admin.display(description='Местоположение')
    def short_location(self, obj):
        return obj.location.name[:SHORT_STANDARD_MIN]

    @admin.display(description='Категория')
    def short_category(self, obj):
        return obj.category.title[:SHORT_STANDARD]

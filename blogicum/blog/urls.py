from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),

    # создание поста
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),

    # показывает одетальный пост
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    # редактирвание публикаций
    path('posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    #  Удаление публикации
    path('posts/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='delete_post'),

    # Добавление коментария
    path('posts/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='add_comment',),
    # Редактирование коментария
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    # Удаление коментария
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', views.CommentDeleteView.as_view(), name='delete_comment'),

    







    path('profile/<slug:username>/', views.UserDetailView.as_view(), name='profile'),  # TODO доделать путь,
    path('category/<slug:category_slug>/', views.PostDetailView.as_view(), name='category_posts'),  # TODO Написать нормальную функцию обработчик

]

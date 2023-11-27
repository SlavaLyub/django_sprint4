from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages'))
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов
    # из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    # Подключаем функцию static() к urlpatterns:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "core.views.page_not_found_view"
handler403 = 'core.views.forbidden'
# handler500 = 'core.views.server_error'

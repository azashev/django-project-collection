from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('book_app_final.core_app.urls')),
    path('profile/', include('book_app_final.users_app.urls')),
    path('books/', include('book_app_final.books_app.urls')),
    path('reviews/', include('book_app_final.reviews_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

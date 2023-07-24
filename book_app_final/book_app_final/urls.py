from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('book_app_final.core_app.urls')),
    path('profile/', include('book_app_final.users_app.urls'))
]

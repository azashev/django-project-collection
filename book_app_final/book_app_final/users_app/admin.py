from django.contrib import admin

from book_app_final.users_app.models import CustomUser, Shelf


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    pass

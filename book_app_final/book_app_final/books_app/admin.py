from django.contrib import admin

from book_app_final.books_app.models import Genre, Author, Book


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    exclude = ('created_by',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    exclude = ('slug',)

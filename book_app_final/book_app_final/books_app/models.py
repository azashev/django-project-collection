from django.db import models
from django.utils.text import slugify

from book_app_final.users_app.models import CustomUser


class Author(models.Model):
    author_name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )

    def __str__(self):
        return self.author_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.author_name)
        super().save(*args, **kwargs)


class Genre(models.Model):
    genre_name = models.CharField(
        max_length=200,
    )

    def __str__(self):
        return self.genre_name


class Book(models.Model):
    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.RESTRICT,
    )

    genres = models.ManyToManyField(
        Genre,
    )

    book_image = models.URLField(
        max_length=200,
        null=False,
        blank=False,
    )

    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='added_books'
    )

    added_on = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.title

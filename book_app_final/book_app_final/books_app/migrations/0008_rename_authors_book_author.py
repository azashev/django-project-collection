# Generated by Django 4.2.3 on 2023-07-27 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0007_remove_book_authors_book_authors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='authors',
            new_name='author',
        ),
    ]

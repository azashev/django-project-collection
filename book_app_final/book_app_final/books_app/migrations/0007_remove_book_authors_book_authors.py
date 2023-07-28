# Generated by Django 4.2.3 on 2023-07-27 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0006_genre_book_added_on_book_book_image_book_genres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='authors',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='books_app.author'),
            preserve_default=False,
        ),
    ]
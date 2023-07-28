from django import forms

from book_app_final.reviews_app.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']
        labels = {
            'review_text': 'Review',
        }

from django import forms

from book_app_final.reviews_app.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']
        labels = {
            'review_text': 'Review',
        }

    # Validation
    def clean_review_text(self):
        review_text = self.cleaned_data.get('review_text')
        if review_text and not review_text.strip():
            raise forms.ValidationError("Review cannot be only whitespace.")
        return review_text

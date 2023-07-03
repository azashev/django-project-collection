from django import forms

from petstagram.core.form_mixins import DisabledFormMixin
from petstagram.photos.models import Photo


class PhotoBaseForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('publication_date',)


class PhotoCreateForm(PhotoBaseForm):
    pass


class PhotoEditForm(PhotoBaseForm):
    class Meta:
        model = Photo
        exclude = ('publication_date', 'photo')


class PhotoDeleteForm(DisabledFormMixin, PhotoBaseForm):
    class Meta:
        model = Photo
        exclude = ('photo', 'tagged_pets',)
        labels = {
            'description': 'Description',
            'location': 'Location',
            'tagged_pets': 'Tagged pets',
        }

    disabled_fields = ('description', 'location', 'tagged_pets')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disable_fields()

    def save(self, commit=True):
        if commit:
            self.instance.photolike_set.all().delete()
            # PhotoLike.objects.filter(photo_id=self.instance.id).delete()
            self.instance.photocomment_set.all().delete()
            # PhotoComment.objects.filter(photo_id=self.instance.id).delete()
            self.instance.delete()
        return self.instance

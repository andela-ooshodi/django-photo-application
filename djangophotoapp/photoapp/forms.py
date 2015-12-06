from django.forms import ModelForm
from .models import Pictures
from cloudinary.forms import CloudinaryFileField


class PicturesForm(ModelForm):

    class Meta:
        model = Pictures
        fields = ['picture']

    picture = CloudinaryFileField(
        options={
            'use_filename': True
        })

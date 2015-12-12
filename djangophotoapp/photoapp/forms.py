from django.forms import ModelForm
from .models import Images
from cloudinary.forms import CloudinaryFileField


class ImageForm(ModelForm):

    class Meta:
        model = Images
        fields = ['image']

    image = CloudinaryFileField(
        options={
            'use_filename': True,
            'allowed_formats': ['jpg', 'png', 'gif', 'tiff', 'bmp']
        })

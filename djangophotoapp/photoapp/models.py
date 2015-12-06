from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.TextField()


class Images(models.Model):
    owner = models.ForeignKey(User)
    image = CloudinaryField('image')
    image_file_name = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='created')

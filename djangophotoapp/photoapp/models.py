from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.TextField()


class Pictures(models.Model):
    owner = models.ForeignKey(User)
    picture = CloudinaryField('picture')
    picture_file_name = models.CharField(max_length=100, null=True)

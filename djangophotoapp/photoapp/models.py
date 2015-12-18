from time import time
from django.db import models
from django.contrib.auth.models import User


def upload_path(instance, filename):
    return 'uploads/%s_%s' % (str(time()).replace('.', '_'), filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.TextField()


class Images(models.Model):
    owner = models.ForeignKey(User)
    image = models.ImageField(upload_to=upload_path)
    image_file_name = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='created')

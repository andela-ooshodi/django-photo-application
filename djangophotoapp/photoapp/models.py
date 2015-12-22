from time import time
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

import os


def upload_path(instance, filename):
    return 'uploads/user_{0}/{1}_{2}'.format(
        instance.owner.id,
        str(time()).replace('.', '_'),
        filename
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.TextField()


class Images(models.Model):
    owner = models.ForeignKey(User)
    image = models.ImageField(upload_to=upload_path)
    image_file_name = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='created')


# Function to delete from the file storage
@receiver(post_delete, sender=Images)
def delete_from_file_system(sender, instance, **kwargs):

    image_path = instance.image.path

    # split the image part
    filepath, ext = os.path.splitext(image_path)
    # create the filtered image path
    new_filepath = filepath + "filtered" + ext
    # delete from file directory

    if os.path.exists(image_path):
        # delete image
        os.remove(image_path)

    if os.path.exists(new_filepath):
        # delete filtered image
        os.remove(new_filepath)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photoapp', '0002_pictures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name=b'image')),
                ('image_file_name', models.CharField(max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'created')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='pictures',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Pictures',
        ),
    ]

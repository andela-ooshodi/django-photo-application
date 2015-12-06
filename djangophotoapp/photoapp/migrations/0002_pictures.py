# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name=b'picture')),
                ('picture_file_name', models.CharField(max_length=100, null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

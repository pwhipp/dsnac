# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.bookrepo.models


class Migration(migrations.Migration):

    dependencies = [
        ('bookrepo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_panjabi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='ebook_file',
            field=models.FileField(null=True, upload_to=apps.bookrepo.models.content_file_name, blank=True),
        ),
    ]

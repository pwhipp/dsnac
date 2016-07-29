# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('colour', colorfield.fields.ColorField(default=b'#7a1315', max_length=10)),
            ],
        ),
    ]

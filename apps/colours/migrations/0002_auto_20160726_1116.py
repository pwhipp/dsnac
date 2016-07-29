# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('colours', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomTheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('header', colorfield.fields.ColorField(default=b'#7a1315', max_length=10)),
                ('body', colorfield.fields.ColorField(default=b'#1e2633', max_length=10)),
                ('links', colorfield.fields.ColorField(default=b'#ffffff', max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='theme',
            name='colour',
        ),
        migrations.AddField(
            model_name='theme',
            name='active',
            field=models.CharField(default=b'default', max_length=255, choices=[(b'default', b'Default'), (b'orange', b'Orange'), (b'green', b'Green')]),
        ),
    ]

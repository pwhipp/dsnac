# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True, blank=True)),
                ('default_card', models.CharField(max_length=255, null=True, blank=True)),
                ('stripe_id', models.CharField(max_length=255, null=True, blank=True)),
                ('card_last', models.CharField(max_length=255, null=True, blank=True)),
                ('card_expiry', models.CharField(max_length=255, null=True, blank=True)),
                ('payment_active', models.BooleanField(default=False)),
                ('subscribe', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.CharField(max_length=255)),
                ('memory_of', models.BooleanField(default=False)),
                ('memory_of_type', models.CharField(blank=True, max_length=255, null=True, choices=[(b'1', b'In Honor Of'), (b'2', b'In Memory Of')])),
                ('first_name_memory', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name_memory', models.CharField(max_length=255, null=True, blank=True)),
                ('full_name_notification', models.CharField(max_length=255, null=True, blank=True)),
                ('from_notification', models.CharField(max_length=255, null=True, blank=True)),
                ('recipient_notification', models.CharField(max_length=255, null=True, blank=True)),
                ('anonymous', models.BooleanField(default=True)),
                ('message_notification', models.CharField(max_length=255, null=True, blank=True)),
                ('cc_first_name', models.CharField(max_length=255)),
                ('cc_last_name', models.CharField(max_length=255)),
                ('bill_street', models.CharField(max_length=255)),
                ('bill_city', models.CharField(max_length=255)),
                ('bill_zip', models.CharField(max_length=255)),
                ('bill_apt', models.CharField(max_length=255, null=True, blank=True)),
                ('bill_state', models.CharField(max_length=255)),
                ('bill_country', models.CharField(max_length=255)),
                ('monthly_gift', models.BooleanField(default=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='userprofile.Profile')),
            ],
            options={
                'verbose_name': 'Donation',
                'verbose_name_plural': 'Donations',
            },
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keywords_string', models.CharField(max_length=500, editable=False, blank=True)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('_meta_title', models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('gen_description', models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description')),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('status', models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True)),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True)),
                ('short_url', models.URLField(null=True, blank=True)),
                ('in_sitemap', models.BooleanField(default=True, verbose_name='Show in sitemap')),
                ('content', mezzanine.core.fields.RichTextField(help_text=b'Brief description of the books content for searching and web display', verbose_name='Content')),
                ('identifier', models.CharField(help_text=b'Unique identifier for this book edition - used as folder name for book related scan and OCR files', unique=True, max_length=255)),
                ('reference', models.CharField(help_text=b'Library reference number', max_length=255, null=True)),
                ('published', models.CharField(help_text=b'Date of publication (text for now)', max_length=32)),
                ('num_pages', models.IntegerField(default=0, help_text=b'Number of scanned or actual pages (scanned pages takes precedence)')),
                ('num_copies', models.IntegerField(default=1, help_text=b'Number of physical copies held by the library')),
                ('scanned', models.BooleanField(default=False)),
                ('scanned_start_page', models.IntegerField(default=0)),
                ('ebook_file', models.FileField(help_text=b'Only zip files accepted', null=True, upload_to=b'books/', blank=True)),
                ('ebook', models.BooleanField(default=False)),
                ('cover', models.ImageField(default=None, null=True, upload_to=b'cover/', blank=True)),
                ('book_type', models.CharField(default=None, choices=[(b'Book', b'Book'), (b'Magazine', b'Magazine'), (b'Document', b'Document')], max_length=255, blank=True, null=True, verbose_name=b'Material Type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField(verbose_name=b'Page number')),
                ('text', models.TextField()),
                ('book', models.ForeignKey(to='bookrepo.Book')),
            ],
        ),
        migrations.CreateModel(
            name='BookUploadLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scanned', models.BooleanField(default=False)),
                ('to_del', models.BooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(to='bookrepo.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=512)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=512)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MainSlider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'Slide name')),
                ('image', models.FileField(upload_to=b'slider/')),
                ('annotation', models.TextField(default=None, null=True, verbose_name=b'annotation', blank=True)),
            ],
            options={
                'verbose_name': 'Slider',
                'verbose_name_plural': 'slides',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=512)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='book',
            name='contributor',
            field=models.ForeignKey(to='bookrepo.Contributor', help_text=b'The organisation or individual who contributed the book to the library', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='creator',
            field=models.ForeignKey(to='bookrepo.Creator', help_text=b'The creator of the book, usually the author or authors but may be the editor or a committee.', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='site',
            field=models.ForeignKey(editable=False, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='book',
            name='subject',
            field=models.ForeignKey(to='bookrepo.Subject', help_text=b'The subject categorization used in the library', null=True),
        ),
    ]

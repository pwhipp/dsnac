# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subject'
        db.create_table(u'bookrepo_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
        ))
        db.send_create_signal(u'bookrepo', ['Subject'])

        # Adding model 'Creator'
        db.create_table(u'bookrepo_creator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
        ))
        db.send_create_signal(u'bookrepo', ['Creator'])

        # Adding model 'Contributor'
        db.create_table(u'bookrepo_contributor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=512)),
        ))
        db.send_create_signal(u'bookrepo', ['Contributor'])

        # Adding model 'Book'
        db.create_table(u'bookrepo_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookrepo.Creator'], null=True)),
            ('contributor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookrepo.Contributor'], null=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('published', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('pages', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('scanned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ebook', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'bookrepo', ['Book'])


    def backwards(self, orm):
        # Deleting model 'Subject'
        db.delete_table(u'bookrepo_subject')

        # Deleting model 'Creator'
        db.delete_table(u'bookrepo_creator')

        # Deleting model 'Contributor'
        db.delete_table(u'bookrepo_contributor')

        # Deleting model 'Book'
        db.delete_table(u'bookrepo_book')


    models = {
        u'bookrepo.book': {
            'Meta': {'object_name': 'Book'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookrepo.Contributor']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookrepo.Creator']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'pages': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'scanned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'bookrepo.contributor': {
            'Meta': {'ordering': "['name']", 'object_name': 'Contributor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        u'bookrepo.creator': {
            'Meta': {'ordering': "['name']", 'object_name': 'Creator'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        u'bookrepo.subject': {
            'Meta': {'ordering': "['name']", 'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '512'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['bookrepo']
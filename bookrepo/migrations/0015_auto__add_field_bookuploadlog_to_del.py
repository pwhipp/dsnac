# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BookUploadLog.to_del'
        db.add_column(u'bookrepo_bookuploadlog', 'to_del',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BookUploadLog.to_del'
        db.delete_column(u'bookrepo_bookuploadlog', 'to_del')


    models = {
        u'bookrepo.book': {
            'Meta': {'object_name': 'Book'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'book_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookrepo.Contributor']", 'null': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookrepo.Creator']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ebook': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ebook_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'num_copies': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'num_pages': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'scanned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scanned_start_page': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookrepo.Subject']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'bookrepo.bookpage': {
            'Meta': {'object_name': 'BookPage'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookrepo.Book']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'bookrepo.bookuploadlog': {
            'Meta': {'object_name': 'BookUploadLog'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookrepo.Book']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'scanned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_del': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        u'bookrepo.mainslider': {
            'Meta': {'object_name': 'MainSlider'},
            'annotation': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
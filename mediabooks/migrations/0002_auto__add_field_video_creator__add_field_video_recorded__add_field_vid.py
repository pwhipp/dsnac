# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Video.creator'
        db.add_column(u'mediabooks_video', 'creator',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Video.recorded'
        db.add_column(u'mediabooks_video', 'recorded',
                      self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Video.duration'
        db.add_column(u'mediabooks_video', 'duration',
                      self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Audio.creator'
        db.add_column(u'mediabooks_audio', 'creator',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Audio.recorded'
        db.add_column(u'mediabooks_audio', 'recorded',
                      self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Audio.duration'
        db.add_column(u'mediabooks_audio', 'duration',
                      self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Video.creator'
        db.delete_column(u'mediabooks_video', 'creator')

        # Deleting field 'Video.recorded'
        db.delete_column(u'mediabooks_video', 'recorded')

        # Deleting field 'Video.duration'
        db.delete_column(u'mediabooks_video', 'duration')

        # Deleting field 'Audio.creator'
        db.delete_column(u'mediabooks_audio', 'creator')

        # Deleting field 'Audio.recorded'
        db.delete_column(u'mediabooks_audio', 'recorded')

        # Deleting field 'Audio.duration'
        db.delete_column(u'mediabooks_audio', 'duration')


    models = {
        u'mediabooks.audio': {
            'Meta': {'object_name': 'Audio'},
            'creator': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mp3': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'recorded': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'mediabooks.video': {
            'Meta': {'object_name': 'Video'},
            'creator': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'recorded': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['mediabooks']
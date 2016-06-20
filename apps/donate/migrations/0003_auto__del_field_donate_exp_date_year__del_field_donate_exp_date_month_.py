# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Donate.exp_date_year'
        db.delete_column(u'donate_donate', 'exp_date_year')

        # Deleting field 'Donate.exp_date_month'
        db.delete_column(u'donate_donate', 'exp_date_month')

        # Deleting field 'Donate.cc_number'
        db.delete_column(u'donate_donate', 'cc_number')


        # Changing field 'Donate.email'
        db.alter_column(u'donate_donate', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75))

    def backwards(self, orm):
        # Adding field 'Donate.exp_date_year'
        db.add_column(u'donate_donate', 'exp_date_year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=15, max_length=2),
                      keep_default=False)

        # Adding field 'Donate.exp_date_month'
        db.add_column(u'donate_donate', 'exp_date_month',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=12, max_length=2),
                      keep_default=False)

        # Adding field 'Donate.cc_number'
        db.add_column(u'donate_donate', 'cc_number',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=255),
                      keep_default=False)


        # Changing field 'Donate.email'
        db.alter_column(u'donate_donate', 'email', self.gf('django.db.models.fields.CharField')(max_length=255))

    models = {
        u'donate.donate': {
            'Meta': {'object_name': 'Donate'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bill_apt': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bill_city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bill_country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bill_state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bill_street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bill_zip': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cc_first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cc_last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name_memory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'from_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_name_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name_memory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'memory_of': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'memory_of_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'message_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'monthly_gift': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'recipient_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['donate']
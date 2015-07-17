# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Donate'
        db.create_table(u'donate_donate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('memory_of', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('memory_of_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('first_name_memory', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name_memory', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('full_name_notification', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('from_notification', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('recipient_notification', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('anonymous', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('message_notification', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('cc_first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cc_last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cc_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('exp_date', self.gf('django.db.models.fields.DateField')()),
            ('bill_street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bill_city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bill_zip', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bill_apt', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('bill_state', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bill_country', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('monthly_gift', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('subscribe', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'donate', ['Donate'])


    def backwards(self, orm):
        # Deleting model 'Donate'
        db.delete_table(u'donate_donate')


    models = {
        u'donate.donate': {
            'Meta': {'object_name': 'Donate'},
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
            'cc_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'exp_date': ('django.db.models.fields.DateField', [], {}),
            'first_name_memory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'from_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_name_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name_memory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'memory_of': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'memory_of_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'message_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'monthly_gift': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'recipient_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['donate']
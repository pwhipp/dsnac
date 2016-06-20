# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Donate.exp_date_year'
        db.delete_column(u'donate_donate', 'exp_date_year')

        # Deleting field 'Donate.subscribe'
        db.delete_column(u'donate_donate', 'subscribe')

        # Deleting field 'Donate.exp_date_month'
        db.delete_column(u'donate_donate', 'exp_date_month')

        # Deleting field 'Donate.cc_number'
        db.delete_column(u'donate_donate', 'cc_number')

        # Deleting field 'Donate.email'
        db.delete_column(u'donate_donate', 'email')

        # Deleting field 'Donate.phone'
        db.delete_column(u'donate_donate', 'phone')

        # Deleting field 'Donate.cc_code'
        db.delete_column(u'donate_donate', 'cc_code')

        # Adding field 'Donate.user'
        db.add_column(u'donate_donate', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['userprofile.Profile']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Donate.exp_date_year'
        db.add_column(u'donate_donate', 'exp_date_year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=2016, max_length=2),
                      keep_default=False)

        # Adding field 'Donate.subscribe'
        db.add_column(u'donate_donate', 'subscribe',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Donate.exp_date_month'
        db.add_column(u'donate_donate', 'exp_date_month',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, max_length=2),
                      keep_default=False)

        # Adding field 'Donate.cc_number'
        db.add_column(u'donate_donate', 'cc_number',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, max_length=16),
                      keep_default=False)

        # Adding field 'Donate.email'
        db.add_column(u'donate_donate', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='email@exaple.com', max_length=75),
                      keep_default=False)

        # Adding field 'Donate.phone'
        db.add_column(u'donate_donate', 'phone',
                      self.gf('django.db.models.fields.CharField')(default=1123123, max_length=255),
                      keep_default=False)

        # Adding field 'Donate.cc_code'
        db.add_column(u'donate_donate', 'cc_code',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=123, max_length=3),
                      keep_default=False)

        # Deleting field 'Donate.user'
        db.delete_column(u'donate_donate', 'user_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'first_name_memory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'from_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_name_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name_memory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'memory_of': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'memory_of_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'message_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'monthly_gift': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recipient_notification': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['userprofile.Profile']"})
        },
        u'userprofile.profile': {
            'Meta': {'object_name': 'Profile'},
            'card_expiry': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'card_last': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'default_card': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stripe_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subscribe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['donate']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rule'
        db.create_table(u'challenge_rule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenge.Challenge'])),
        ))
        db.send_create_signal(u'challenge', ['Rule'])


    def backwards(self, orm):
        # Deleting model 'Rule'
        db.delete_table(u'challenge_rule')


    models = {
        u'challenge.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'rules': ('django.db.models.fields.TextField', [], {}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        u'challenge.rule': {
            'Meta': {'object_name': 'Rule'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenge.Challenge']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['challenge']
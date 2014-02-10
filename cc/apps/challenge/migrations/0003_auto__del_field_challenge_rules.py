# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Challenge.rules'
        db.delete_column(u'challenge_challenge', 'rules')


    def backwards(self, orm):
        # Adding field 'Challenge.rules'
        db.add_column(u'challenge_challenge', 'rules',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    models = {
        u'challenge.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
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
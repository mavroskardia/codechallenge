# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Challenge.end'
        db.delete_column(u'challenge_challenge', 'end')

        # Deleting field 'Challenge.start'
        db.delete_column(u'challenge_challenge', 'start')


    def backwards(self, orm):
        # Adding field 'Challenge.end'
        db.add_column(u'challenge_challenge', 'end',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'Challenge.start'
        db.add_column(u'challenge_challenge', 'start',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)


    models = {
        u'challenge.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'challenge.rule': {
            'Meta': {'object_name': 'Rule'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['challenge.Challenge']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['challenge']
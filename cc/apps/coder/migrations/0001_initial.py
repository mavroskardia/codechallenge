# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Coder'
        db.create_table(u'coder_coder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('tagline', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('about', self.gf('django.db.models.fields.TextField')()),
            ('xp', self.gf('django.db.models.fields.BigIntegerField')()),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coder.Level'])),
        ))
        db.send_create_signal(u'coder', ['Coder'])

        # Adding M2M table for field challenges on 'Coder'
        m2m_table_name = db.shorten_name(u'coder_coder_challenges')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('coder', models.ForeignKey(orm[u'coder.coder'], null=False)),
            ('challenge', models.ForeignKey(orm[u'challenge.challenge'], null=False))
        ))
        db.create_unique(m2m_table_name, ['coder_id', 'challenge_id'])

        # Adding model 'Level'
        db.create_table(u'coder_level', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('starting_xp', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal(u'coder', ['Level'])


    def backwards(self, orm):
        # Deleting model 'Coder'
        db.delete_table(u'coder_coder')

        # Removing M2M table for field challenges on 'Coder'
        db.delete_table(db.shorten_name(u'coder_coder_challenges'))

        # Deleting model 'Level'
        db.delete_table(u'coder_level')


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
        u'coder.coder': {
            'Meta': {'object_name': 'Coder'},
            'about': ('django.db.models.fields.TextField', [], {}),
            'challenges': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['challenge.Challenge']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['coder.Level']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'xp': ('django.db.models.fields.BigIntegerField', [], {})
        },
        u'coder.level': {
            'Meta': {'object_name': 'Level'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'starting_xp': ('django.db.models.fields.BigIntegerField', [], {})
        }
    }

    complete_apps = ['coder']
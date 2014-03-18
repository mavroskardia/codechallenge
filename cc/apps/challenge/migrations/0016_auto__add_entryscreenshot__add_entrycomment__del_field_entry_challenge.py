# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntryScreenshot'
        db.create_table('challenge_entryscreenshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenge.Entry'])),
            ('pic', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('challenge', ['EntryScreenshot'])

        # Adding model 'EntryComment'
        db.create_table('challenge_entrycomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenge.Entry'])),
            ('coder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['coder.Coder'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 13, 0, 0))),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('challenge', ['EntryComment'])

        # Deleting field 'Entry.challenge'
        db.delete_column('challenge_entry', 'challenge_id')


    def backwards(self, orm):
        # Deleting model 'EntryScreenshot'
        db.delete_table('challenge_entryscreenshot')

        # Deleting model 'EntryComment'
        db.delete_table('challenge_entrycomment')


        # User chose to not deal with backwards NULL issues for 'Entry.challenge'
        raise RuntimeError("Cannot reverse this migration. 'Entry.challenge' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Entry.challenge'
        db.add_column('challenge_entry', 'challenge',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['challenge.Challenge']),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'challenge.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coder.Coder']"})
        },
        'challenge.challengecomment': {
            'Meta': {'object_name': 'ChallengeComment'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Challenge']"}),
            'coder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coder.Coder']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'challenge.entry': {
            'Meta': {'object_name': 'Entry'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Participant']"}),
            'thefile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'challenge.entrycomment': {
            'Meta': {'object_name': 'EntryComment'},
            'coder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coder.Coder']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 13, 0, 0)'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'challenge.entryscreenshot': {
            'Meta': {'object_name': 'EntryScreenshot'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'challenge.participant': {
            'Meta': {'unique_together': "(('coder', 'challenge'),)", 'object_name': 'Participant'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Challenge']"}),
            'coder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coder.Coder']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_owner': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'challenge.rule': {
            'Meta': {'object_name': 'Rule'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Challenge']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'coder.coder': {
            'Meta': {'object_name': 'Coder'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']"}),
            'xp': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['challenge']
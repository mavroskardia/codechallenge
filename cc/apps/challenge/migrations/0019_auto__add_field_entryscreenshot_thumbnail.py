# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from io import BytesIO
from PIL import Image
from django.core.files import File


class Migration(SchemaMigration):

    def get_default_image(self):
        fakefile = BytesIO()

        img = Image.new('RGB', (100,100))
        img.save(fakefile, format='png')

        return File(fakefile)


    def forwards(self, orm):
        # Adding field 'EntryScreenshot.thumbnail'
        db.add_column('challenge_entryscreenshot', 'thumbnail',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, default=self.get_default_image),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EntryScreenshot.thumbnail'
        db.delete_column('challenge_entryscreenshot', 'thumbnail')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
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
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 15, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'challenge.entry': {
            'Meta': {'object_name': 'Entry'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Challenge']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 15, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Participant']"}),
            'thefile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'challenge.entrycomment': {
            'Meta': {'object_name': 'EntryComment'},
            'coder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coder.Coder']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 15, 0, 0)'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'challenge.entryscreenshot': {
            'Meta': {'object_name': 'EntryScreenshot'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'challenge.participant': {
            'Meta': {'object_name': 'Participant', 'unique_together': "(('coder', 'challenge'),)"},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['challenge.Challenge']"}),
            'coder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['coder.Coder']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 3, 15, 0, 0)'}),
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
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '256'}),
            'tagline': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '1024'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'xp': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['challenge']
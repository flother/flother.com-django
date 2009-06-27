import django
from django.db import models
from south.db import db

from flother.apps.contact.models import *


class Migration:
    def forwards(self, orm):
        """Add model ``Message``."""
        db.create_table('contact_message', (
            ('body', orm['contact.Message:body']),
            ('sender_name', orm['contact.Message:sender_name']),
            ('created_at', orm['contact.Message:created_at']),
            ('updated_at', orm['contact.Message:updated_at']),
            ('sender_email', orm['contact.Message:sender_email']),
            ('id', orm['contact.Message:id']),
            ('is_spam', orm['contact.Message:is_spam']),
        ))
        db.send_create_signal('contact', ['Message'])

    def backwards(self, orm):
        """Delete model ``Message``."""
        db.delete_table('contact_message')

    models = {
        'contact.message': {
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'blank': 'True'}),
            'is_spam': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'sender_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['contact']

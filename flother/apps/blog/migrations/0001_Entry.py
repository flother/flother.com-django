import django
from django.db import models
from south.db import db

from flother.apps.blog.models import Entry


class Migration:
    def forwards(self, orm):
        """Add model ``Entry``."""
        db.create_table('blog_entry', (
            ('standfirst', orm['blog.Entry:standfirst']),
            ('status', orm['blog.Entry:status']),
            ('author', orm['blog.Entry:author']),
            ('created_at', orm['blog.Entry:created_at']),
            ('title', orm['blog.Entry:title']),
            ('updated_at', orm['blog.Entry:updated_at']),
            ('id', orm['blog.Entry:id']),
            ('published_at', orm['blog.Entry:published_at']),
            ('number_of_views', orm['blog.Entry:number_of_views']),
            ('copy', orm['blog.Entry:copy']),
            ('slug', orm['blog.Entry:slug']),
        ))
        db.send_create_signal('blog', ['Entry'])

    def backwards(self, orm):
        """Delete model ``Entry``."""
        db.delete_table('blog_entry')

    models = {
        'blog.entry': {
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'copy': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'blank': 'True'}),
            'number_of_views': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'standfirst': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['blog']

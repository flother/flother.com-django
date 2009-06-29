import django
from django.db import models
from south.db import db

from flother.apps.blog.models import Entry


class Migration:

    """Add the field ``enable_comments`` to the ``Entry`` model."""

    def forwards(self, orm):
        """Add field ``Entry.enable_comments``."""
        db.add_column('blog_entry', 'enable_comments', orm['blog.Entry:enable_comments'])

    def backwards(self, orm):
        """Delete field ``Entry.enable_comments``."""
        db.delete_column('blog_entry', 'enable_comments')

    models = {
        'blog.entry': {
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'copy': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'blank': 'True'}),
            'number_of_views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 6, 29, 14, 50, 25, 986127)'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'standfirst': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
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

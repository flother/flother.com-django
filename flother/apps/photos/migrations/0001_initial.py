import datetime

from django.db import models
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Photo'
        db.create_table('photos_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('original', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('medium', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('listing', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('photographer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=2)),
            ('exposure', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('aperture', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('focal_length', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('iso_speed', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('taken_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('uploaded_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_landscape', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['places.Point'], null=True, blank=True)),
            ('camera', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Camera'], null=True, blank=True)),
        ))
        db.send_create_signal('photos', ['Photo'])

        # Adding M2M table for field collections on 'Photo'
        db.create_table('photos_photo_collections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm['photos.photo'], null=False)),
            ('collection', models.ForeignKey(orm['photos.collection'], null=False))
        ))
        db.create_unique('photos_photo_collections', ['photo_id', 'collection_id'])

        # Adding model 'Collection'
        db.create_table('photos_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, db_index=True)),
            ('key_photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('photos', ['Collection'])

        # Adding model 'Camera'
        db.create_table('photos_camera', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, db_index=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('photos', ['Camera'])

        # Adding model 'FlickrPhoto'
        db.create_table('photos_flickrphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photos.Photo'], null=True, blank=True)),
            ('flickr_id', self.gf('django.db.models.fields.TextField')(max_length=128, db_index=True)),
        ))
        db.send_create_signal('photos', ['FlickrPhoto'])


    def backwards(self, orm):
        # Deleting model 'Photo'
        db.delete_table('photos_photo')

        # Removing M2M table for field collections on 'Photo'
        db.delete_table('photos_photo_collections')

        # Deleting model 'Collection'
        db.delete_table('photos_collection')

        # Deleting model 'Camera'
        db.delete_table('photos_camera')

        # Deleting model 'FlickrPhoto'
        db.delete_table('photos_flickrphoto')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'photos.camera': {
            'Meta': {'object_name': 'Camera'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'})
        },
        'photos.collection': {
            'Meta': {'object_name': 'Collection'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'photos.flickrphoto': {
            'Meta': {'object_name': 'FlickrPhoto'},
            'flickr_id': ('django.db.models.fields.TextField', [], {'max_length': '128', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['photos.Photo']", 'null': 'True', 'blank': 'True'})
        },
        'photos.photo': {
            'Meta': {'object_name': 'Photo'},
            'aperture': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'camera': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['photos.Camera']", 'null': 'True', 'blank': 'True'}),
            'collections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['photos.Collection']", 'symmetrical': 'False', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'exposure': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'focal_length': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_landscape': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'iso_speed': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'listing': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'medium': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'photographer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Point']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '2'}),
            'taken_at': ('django.db.models.fields.DateTimeField', [], {}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'places.country': {
            'Meta': {'object_name': 'Country'},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True'}),
            'flag': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'formal_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'places.location': {
            'Meta': {'unique_together': "(('slug', 'country'),)", 'object_name': 'Location'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'places.point': {
            'Meta': {'unique_together': "(('longitude', 'latitude', 'accuracy'),)", 'object_name': 'Point'},
            'accuracy': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '5'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.Location']"}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '5'})
        }
    }

    complete_apps = ['photos']

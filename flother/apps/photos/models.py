import os
import hashlib

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.utils.html import escape
from PIL import Image, ImageFile

from flother.apps.places.models import Point
from flother.utils.image import create_thumbnail


class Photo(models.Model):

    """A photograph in various sizes along with its metadata."""

    MEDIUM_LANDSCAPE_SIZE = [606, 404]
    MEDIUM_PORTRAIT_SIZE = [404, 606]
    LISTING_SIZE = (300, 200)
    THUMBNAIL_SIZE = (128, 128)
    ORIGINAL_UPLOAD_DIRECTORY = 'apps/photos/originals'
    MEDIUM_UPLOAD_DIRECTORY = 'apps/photos/medium'
    LISTING_UPLOAD_DIRECTORY = 'apps/photos/listing'
    THUMBNAIL_UPLOAD_DIRECTORY = 'apps/photos/thumbnails'

    PUBLISHED_STATUS = 2
    PRIVATE_STATUS = 3
    STATUS_CHOICES = ((PUBLISHED_STATUS, 'Published'),
        (PRIVATE_STATUS, 'Private'))

    title = models.CharField(max_length=128)
    slug = models.SlugField(unique_for_year='taken_at')
    original = models.ImageField(upload_to=ORIGINAL_UPLOAD_DIRECTORY,
        verbose_name='image')
    medium = models.ImageField(upload_to=MEDIUM_UPLOAD_DIRECTORY, blank=True)
    listing = models.ImageField(upload_to=LISTING_UPLOAD_DIRECTORY, blank=True)
    thumbnail = models.ImageField(upload_to=THUMBNAIL_UPLOAD_DIRECTORY,
        blank=True)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    photographer = models.ForeignKey(User)
    status = models.SmallIntegerField(choices=STATUS_CHOICES,
        default=PUBLISHED_STATUS)
    exposure = models.CharField(max_length=64, blank=True)
    aperture = models.CharField(max_length=64, blank=True)
    focal_length = models.CharField(max_length=64, blank=True)
    iso_speed = models.CharField(max_length=64, verbose_name='ISO speed',
        blank=True)
    taken_at = models.DateTimeField(verbose_name='date taken')
    uploaded_at = models.DateTimeField(auto_now_add=True,
        verbose_name='date uploaded')
    updated_at = models.DateTimeField(auto_now=True,
        verbose_name='date updated')
    is_landscape = models.BooleanField(default=True)
    collections = models.ManyToManyField('Collection', blank=True, null=True)
    point = models.ForeignKey(Point, blank=True, null=True)
    camera = models.ForeignKey('Camera', blank=True, null=True)

    class Meta:
        get_latest_by = 'taken_at'
        ordering = ('-taken_at',)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        """Return the canonical URL for a photo."""
        from flother.apps.photos.views import photo_detail
        return (photo_detail, (self.taken_at.year, self.slug))

    def save(self, force_insert=False, force_update=False):
        """
        Save the photo.  Overrides the model's default ``save`` method
        to save the original photo in various dimensions.  Each size is
        used in different parts of the site.  The original photo is also
        kept.
        """
        super(Photo, self).save(force_insert, force_update)

        self._set_orientation()
        medium_size = Photo.MEDIUM_LANDSCAPE_SIZE
        if not self.is_landscape:
            medium_size = Photo.MEDIUM_PORTRAIT_SIZE
        image_basename = '%s.jpg' % hashlib.sha1(str(self.id)).hexdigest()
        im = Image.open(self.original.path)
        # Workaround for a problem in the PIL JPEG library:
        # http://mail.python.org/pipermail/image-sig/1999-August/000816.html.
        ImageFile.MAXBLOCK = 1000000

        image_presets = {
            'medium': {'field': self.medium, 'size': medium_size,
                'upload_directory': Photo.MEDIUM_UPLOAD_DIRECTORY},
            'listing': {'field': self.listing, 'size': Photo.LISTING_SIZE,
                'upload_directory': Photo.LISTING_UPLOAD_DIRECTORY},
            'thumbnail': {'field': self.thumbnail, 'size': Photo.THUMBNAIL_SIZE,
                'upload_directory': Photo.THUMBNAIL_UPLOAD_DIRECTORY},
        }
        for preset_name, preset in image_presets.items():
            if preset_name == 'medium':
                image = im
                image.thumbnail(preset['size'], Image.ANTIALIAS)
            else:
                image = create_thumbnail(im, preset['size'])
            image.save(os.path.join(settings.MEDIA_ROOT,
                preset['upload_directory'], image_basename), format="JPEG",
                quality=85, optimize=True)
            preset['file'] = os.path.join(preset['upload_directory'],
                image_basename)

        self.medium = image_presets['medium']['file']
        self.listing = image_presets['listing']['file']
        self.thumbnail = image_presets['thumbnail']['file']

        super(Photo, self).save(force_insert, force_update)

    def is_published(self):
        """
        Returns a boolean denoting whether the photo is publicly
        available.
        """
        return self.status == self.PUBLISHED_STATUS

    def get_previous_published_photo(self):
        """Return the previously published photo by date."""
        return self.get_previous_by_taken_at(status=self.PUBLISHED_STATUS,
            taken_at__lte=datetime.datetime.now)

    def get_next_published_photo(self):
        """Return the next published photo by date."""
        return self.get_next_by_taken_at(status=self.PUBLISHED_STATUS,
            taken_at__lte=datetime.datetime.now)

    def thumbnail_html(self):
        """Return an XHTML image element for the file's thumbnail."""
        return '<img alt="%s" height="%s" src="%s" width="%s" />' % (
            escape(self.title), Photo.THUMBNAIL_SIZE[1],
            escape(self.thumbnail.url),  Photo.THUMBNAIL_SIZE[0])
    thumbnail_html.short_description = 'Thumbnail'
    thumbnail_html.allow_tags = True

    def location(self):
        """Return the linked ``Location`` for this photo."""
        return self.point.location

    def _set_orientation(self):
        """
        Set a boolean denoting whther this photo is landscape or
        portrait.
        """
        fp = open(self.original.path, 'rb')
        im = Image.open(fp)
        im.load()
        fp.close()
        if (im.size[1] / float(im.size[0])) > 1:
            self.is_landscape = False
        else:
            self.is_landscape = True


class Collection(models.Model):

    """A collection, or set, of photos."""

    KEY_PHOTO_UPLOAD_DIRECTORY = 'apps/photos/collections'
    KEY_PHOTO_SIZE = (293, 195)

    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    key_photo = models.ImageField(upload_to=KEY_PHOTO_UPLOAD_DIRECTORY)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        """
        Save the collection.  Overrides the model's default ``save``
        method to save the key photo for the collection at the correct
        size.
        """
        super(Collection, self).save(force_insert, force_update)
        im = Image.open(self.key_photo.path)
        if not im.size == Collection.KEY_PHOTO_SIZE:
            image = create_thumbnail(im, Collection.KEY_PHOTO_SIZE)
            image.save(self.key_photo.path, format="JPEG", quality=85,
                optimize=True)
        super(Collection, self).save(force_insert, force_update)

    def number_of_photos(self):
        """Returns the number of photos linked to this collection."""
        return self.photo_set.count()


class Camera(models.Model):

    """A photographic camera used to take the photos on the site."""

    ICON_UPLOAD_DIRECTORY = 'apps/photos/cameras'

    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to=ICON_UPLOAD_DIRECTORY, blank=True)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def number_of_photos(self):
        """Returns the number of photos linked to this camera."""
        return self.photo_set.count()


class FlickrPhoto(models.Model):

    """
    A private model used to track which photos have been imported to the
    site from Flickr.  This model is only for use by the
    ``import_from_flickr`` management command.
    """

    photo = models.ForeignKey(Photo, blank=True, null=True)
    flickr_id = models.TextField(max_length=128, db_index=True)

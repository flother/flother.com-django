import os
import hashlib

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink
from django.utils.html import escape
from PIL import Image, ImageFile

from flother.utils.image import create_thumbnail


class Photo(models.Model):

    MEDIUM_SIZE = [940, 626]
    LISTING_SIZE = (293, 195)
    THUMBNAIL_SIZE = (80, 80)
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
    people = models.ManyToManyField('Person', blank=True, null=True)
    point = models.ForeignKey('Point', blank=True, null=True)
    camera = models.ForeignKey('Camera', blank=True, null=True)

    class Meta:
        get_latest_by = 'taken_at'
        ordering = ('-taken_at',)

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        from flother.apps.photos.views import photo_detail
        return (entry_detail, (self.taken_at.year, self.slug))

    def save(self, force_insert=False, force_update=False):
        super(Photo, self).save(force_insert, force_update)

        self._set_orientation()
        medium_size = Photo.MEDIUM_SIZE
        if not self.is_landscape:
            medium_size.reverse()
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
        for preset in image_presets.values():
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
        return self.status == self.PUBLISHED_STATUS

    def get_previous_published_photo(self):
        return self.get_previous_by_taken_at(status=self.PUBLISHED_STATUS,
            taken_at__lte=datetime.datetime.now)

    def get_next_published_photo(self):
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
        return self.point.location

    def _set_orientation(self):
        fp = open(self.original.path, 'rb')
        im = Image.open(fp)
        im.load()
        fp.close()
        if (im.size[1] / im.size[0]):
            self.is_landscape = False
        else:
            self.is_landscape = True


class Collection(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        pass
        get_latest_by = 'created_at'
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.title

    def number_of_photos(self):
        return self.photo_set.count()


class Point(models.Model):
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    accuracy = models.SmallIntegerField(blank=True, null=True)
    location = models.ForeignKey('Location')

    class Meta:
        unique_together = ('longitude', 'latitude', 'accuracy')
        ordering = ('location', 'longitude', 'latitude')

    def __unicode__(self):
        return unicode(self.location)

    def number_of_photos(self):
        return self.photo_set.count()


class Location(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    country = models.ForeignKey('Country')

    class Meta:
        unique_together = ('slug', 'country')
        ordering = ('country__name', 'name')

    def __unicode__(self):
        return "%s, %s" % (self.name, self.country)

    def number_of_photos(self):
        return Photo.objects.filter(point__location=self).count()


class Country(models.Model):

    FLAG_UPLOAD_DIRECTORY = 'apps/photos/flags'

    name = models.CharField(max_length=32)
    country_code = models.CharField(max_length=2, unique=True)
    formal_name = models.CharField(max_length=128, blank=True)
    flag = models.ImageField(upload_to=FLAG_UPLOAD_DIRECTORY, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'countries'

    def __unicode__(self):
        return self.name

    def number_of_photos(self):
        return Photo.objects.filter(point__location__country=self).count()


class Camera(models.Model):

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
        return self.photo_set.count()


class Person(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    url = models.URLField(blank=True, verify_exists=True, verbose_name='URL')

    class Meta:
        verbose_name_plural = 'people'
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def number_of_photos(self):
        return self.photo_set.count()


class FlickrPhoto(models.Model):
    photo = models.ForeignKey(Photo, blank=True, null=True)
    flickr_id = models.TextField(max_length=128, db_index=True)

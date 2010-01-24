from django.db import models


class Point(models.Model):

    """
    A geographical position specified by a longitude and latitude point.
    It's linked to a ``Location`` model object which is a human name for
    the town or area.  The ``accuracy`` field stores the level of detail
    for the point.
    """

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
        """Returns the number of photos linked to this point."""
        return self.photo_set.count()


class Location(models.Model):

    """A town or city within a particular country."""

    name = models.CharField(max_length=64)
    slug = models.SlugField()
    country = models.ForeignKey('Country')

    class Meta:
        unique_together = ('slug', 'country')
        ordering = ('country__name', 'name')

    def __unicode__(self):
        return "%s, %s" % (self.name, self.country)

    def number_of_photos(self):
        """Returns the number of photos linked to this location."""
        from flother.apps.photos.models import Photo
        return Photo.objects.filter(point__location=self).count()


class Country(models.Model):

    """A country.  It's fairly obvious."""

    FLAG_UPLOAD_DIRECTORY = 'apps/places/flags'

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
        """Returns the number of photos linked to this country."""
        from flother.apps.photos.models import Photo
        return Photo.objects.filter(point__location__country=self).count()

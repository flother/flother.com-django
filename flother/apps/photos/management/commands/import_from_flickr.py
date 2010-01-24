import datetime
import os
import unicodedata
import urllib2

from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.management.base import NoArgsCommand
from django.utils import simplejson
import Flickr.API

from flother.apps.photos.models import Photo, FlickrPhoto, Camera
from flother.apps.places.models import Point, Location, Country
from flother.utils import geonames


class Command(NoArgsCommand):
    help = "Imports photos from Flickr."
    api = None
    default_args = {'format': 'json', 'nojsoncallback': 1}

    def __init__(self):
        self.photographer = User.objects.get(id=1)
        self.api = Flickr.API.API(settings.FLICKR_API_KEY,
            secret=settings.FLICKR_API_SECRET)

    def handle_noargs(self, **options):
        """
        Import photos from a Flickr account and store them and their
        metadata in this site's database.
        """
        verbosity = int(options.get('verbosity', 1))
        page = 0
        last_page = 1
        new_photo_on_this_page = True
        while page < last_page and (new_photo_on_this_page or page == 1):
            # Loop through all the pages in the API results from Flickr.
            # The script will stop before the end if a page has no new
            # photos.
            new_photo_on_this_page = False
            page = page + 1
            photos_json = self.call(method='flickr.people.getPublicPhotos',
                args={'user_id': settings.FLICKR_NSID, 'page': page}).read()
            photos = simplejson.loads(photos_json)
            last_page = photos['photos']['pages']
            for photo_data in photos['photos']['photo']:
                # Does the photo exist?
                flickr_photo, created = FlickrPhoto.objects.select_related().get_or_create(
                    flickr_id=photo_data['id'])
                if created:
                    # It's a new photo!  Let's grab all the metadata.
                    photo_info = simplejson.loads(self.call(
                        method='flickr.photos.getInfo',
                        args={'photo_id': photo_data['id']}).read())
                    photo = Photo()
                    # Because we've found at least one new photo on this
                    # page of results, we'll check the next page too.
                    new_photo_on_this_page = True
                    photo_exif = simplejson.loads(self.call(
                            method='flickr.photos.getExif',
                            args={'photo_id': photo_data['id']}).read())

                    # Add all the metadata to this ``Photo`` model.
                    photo.title = photo_info['photo']['title']['_content'][:128]
                    photo.slug = slugify(photo.title[:50])
                    photo.original = self._save_photo(
                        self._get_photo_data(photo_info), '%s.%s' % (
                        photo_info['photo']['id'],
                        photo_info['photo']['originalformat']))
                    photo.description = photo_info['photo']['description']['_content']
                    photo.photographer = self.photographer
                    photo.exposure = self._get_exif(photo_exif, 'Exposure')[:64]
                    photo.aperture = self._get_exif(photo_exif, 'Aperture')[:64]
                    photo.focal_length = self._get_exif(photo_exif, 'Focal Length')[:64]
                    photo.iso_speed = self._get_exif(photo_exif, 'ISO Speed')[:64]
                    photo.taken_at = self._convert_time(photo_info['photo']['dates']['taken'])
                    photo.uploaded_at = self._convert_time(photo_info['photo']['dateuploaded'])
                    photo.point = self._get_or_create_point(photo_data)
                    # Create a ``Camera`` model for the camera used to
                    # take this photo if it doesnt exist already.
                    camera = self._get_exif(photo_exif, 'Model')[:64]
                    if camera:
                        photo.camera, camera_created = Camera.objects.get_or_create(
                            name=camera, slug=slugify(camera[:50]))
                    photo.save()
                    new_photo_on_this_page = True
                    if not flickr_photo.photo:
                        flickr_photo.photo = photo
                        flickr_photo.save()
                    print unicodedata.normalize('NFKD', unicode(photo.title)).encode(
                        'ascii', 'ignore')

    def call(self, method, args={}, sign=False):
        args.update(self.default_args)
        return self.api.execute_method(method=method, args=args, sign=sign)

    def _convert_time(self, time):
        """
        Convert the date/time string returned by Flickr into a
        ``datetime`` object.
        """
        try:
            converted_time = int(time)
        except ValueError:
            converted_time = datetime.datetime.strptime(time,
                '%Y-%m-%d %H:%M:%S')
        return converted_time

    def _get_exif(self, photo_info, exif_name):
        """
        Return the data stored in an EXIF field, or a blank string if it
        doesn't exist.
        """
        for exif in photo_info['photo']['exif']:
            if exif['label'] == exif_name:
                return exif['raw']['_content']
        return ''

    def _get_or_create_point(self, photo_data):
        """
        Create a ``Point`` model object for use with a newly-imported
        photo.  Creating a point will also create ``Location`` and
        ``Country`` objects as required, and link the ``Point`` to both.
        """
        latlon = simplejson.loads(self.call(
            method='flickr.photos.geo.getLocation',
            args={'photo_id': photo_data['id']}).read())
        if latlon['stat'] == 'ok':
            try:
                point = Point.objects.get(
                    latitude=str('%3.5f' % float(latlon['photo']['location']['latitude'])),
                    longitude=str('%3.5f' % float(latlon['photo']['location']['longitude'])))
                created = False
            except Point.DoesNotExist:
                point = Point(
                    latitude=str('%3.5f' % float(latlon['photo']['location']['latitude'])),
                    longitude=str('%3.5f' % float(latlon['photo']['location']['longitude'])),
                    accuracy=latlon['photo']['location']['accuracy'])
                created = True
            if created:
                # Create location and country.
                try:
                    place = geonames.findNearbyPlaceName(float(point.latitude),
                        float(point.longitude)).geoname[0]
                except AttributeError:
                    return None
                country, created = Country.objects.get_or_create(
                    name=place.countryName, country_code=place.countryCode)
                location, created = Location.objects.get_or_create(
                    name=place.name, slug=slugify(place.name[:50]),
                    country=country)
                location.country = country
                location.save()
                point.location = location
                point.save()
            return point
        return None

    def _get_photo_url(self, photo_info):
        """Return the Flickr URL for a photo."""
        return "http://farm%s.static.flickr.com/%s/%s_%s_o.%s" % (
            photo_info['photo']['farm'], photo_info['photo']['server'],
            photo_info['photo']['id'], photo_info['photo']['originalsecret'],
            photo_info['photo']['originalformat'])

    def _get_photo_data(self, photo_info):
        """Return the raw image (JPEG, GIF, PNG) data from a Flickr."""
        url = self._get_photo_url(photo_info)
        response = urllib2.urlopen(url)
        data = response.read()
        return data

    def _save_photo(self, photo_data, basename):
        """Save the raw photo data taken from Flickr as a file on disk."""
        filename = os.path.join(settings.MEDIA_ROOT,
            Photo.ORIGINAL_UPLOAD_DIRECTORY, basename)
        fh = open(filename, 'w')
        fh.write(photo_data)
        fh.close()
        return os.path.join(Photo.ORIGINAL_UPLOAD_DIRECTORY, basename)

import datetime
import os
import urllib2

from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.management.base import NoArgsCommand
from django.utils import simplejson
import Flickr.API

from flother.apps.photos.models import Photo, FlickrPhoto, Camera, Point,\
    Location, Country
from flother.utils.googlemaps import GoogleMaps


class Command(NoArgsCommand):
    help = "Imports photos from Flickr."
    api = None
    default_args = {'format': 'json', 'nojsoncallback': 1}

    def __init__(self):
        self.photographer = User.objects.get(id=1)
        self.api = Flickr.API.API(settings.FLICKR_API_KEY,
            secret=settings.FLICKR_API_SECRET)
        self.gmaps = GoogleMaps(settings.GOOGLE_MAPS_API_KEY)

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', 1))
        page = 0
        last_page = 1
        new_photo_on_this_page = True
        while page < last_page and new_photo_on_this_page:
            new_photo_on_this_page = False
            page = page + 1
            photos_json = self.call(method='flickr.people.getPublicPhotos',
                args={'user_id': settings.FLICKR_NSID}).read()
            photos = simplejson.loads(photos_json)
            last_page = photos['photos']['pages']
            for photo_data in photos['photos']['photo']:
                flickr_photo, created = FlickrPhoto.objects.select_related().get_or_create(
                    flickr_id=photo_data['id'])
                if created:
                    photo_info = simplejson.loads(self.call(
                        method='flickr.photos.getInfo',
                        args={'photo_id': photo_data['id']}).read())
                    photo = Photo()
                    new_photo_on_this_page = True
                    photo_exif = simplejson.loads(self.call(
                            method='flickr.photos.getExif',
                            args={'photo_id': photo_data['id']}).read())

                    photo.title = photo_info['photo']['title']['_content']
                    photo.slug = slugify(photo.title)
                    photo.original = self._save_photo(
                        self._get_photo_data(photo_info), '%s.%s' % (
                        photo_info['photo']['id'],
                        photo_info['photo']['originalformat']))
                    photo.description = photo_info['photo']['description']['_content']
                    photo.photographer = self.photographer
                    photo.exposure = self._get_exif(photo_exif, 'Exposure')
                    photo.aperture = self._get_exif(photo_exif, 'Aperture')
                    photo.focal_length = self._get_exif(photo_exif, 'Focal Length')
                    photo.iso_speed = self._get_exif(photo_exif, 'ISO Speed')
                    photo.taken_at = self._convert_time(photo_info['photo']['dates']['taken'])
                    photo.uploaded_at = self._convert_time(photo_info['photo']['dateuploaded'])
                    photo.point = self._get_or_create_point(photo_data)
                    camera = self._get_exif(photo_exif, 'Model')
                    if camera:
                        photo.camera, camera_created = Camera.objects.get_or_create(
                            name=camera, slug=slugify(camera))
                    photo.save()
                    if not flickr_photo.photo:
                        flickr_photo.photo = photo
                        flickr_photo.save()
                    print photo.title

    def call(self, method, args={}, sign=False):
        args.update(self.default_args)
        return self.api.execute_method(method=method, args=args, sign=sign)

    def _convert_time(self, time):
        try:
            converted_time = int(time)
        except ValueError:
            converted_time = datetime.datetime.strptime(time,
                '%Y-%m-%d %H:%M:%S')
        return converted_time

    def _get_exif(self, photo_info, exif_name):
        for exif in photo_info['photo']['exif']:
            if exif['label'] == exif_name:
                return exif['raw']['_content']
        return ''

    def _get_or_create_point(self, photo_data):
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
                place = self.gmaps.latlng_to_address(float(point.latitude),
                    float(point.longitude))
                places = place.split(',')
                if len(places) >= 2:
                    country, created = Country.objects.get_or_create(
                        short_name=places[-1].strip())
                    if len(places) == 2:
                        name = places[-2].strip()
                    else:
                        name = places[-3].strip()
                    location, created = Location.objects.get_or_create(
                        name=name, slug=slugify(name), country=country)
                    location.country = country
                    location.save()
                    point.location = location
                    point.save()
            return point
        return None

    def _get_photo_url(self, photo_info):
        return "http://farm%s.static.flickr.com/%s/%s_%s_o.%s" % (
            photo_info['photo']['farm'], photo_info['photo']['server'],
            photo_info['photo']['id'], photo_info['photo']['originalsecret'],
            photo_info['photo']['originalformat'])

    def _get_photo_data(self, photo_info):
        url = self._get_photo_url(photo_info)
        response = urllib2.urlopen(url)
        data = response.read()
        return data

    def _save_photo(self, photo_data, basename):
        filename = os.path.join(settings.MEDIA_ROOT,
            Photo.ORIGINAL_UPLOAD_DIRECTORY, basename)
        fh = open(filename, 'w')
        fh.write(photo_data)
        fh.close()
        return os.path.join(Photo.ORIGINAL_UPLOAD_DIRECTORY, basename)

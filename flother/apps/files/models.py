import datetime
import mimetypes
import os

from django.conf import settings
from django.db import models
from django.utils.html import escape
from PIL import Image

from flother.apps.files.managers import FileManager
from flother.utils.image import create_thumbnail


class File(models.Model):

    """An individual file and its metadata."""

    THUMBNAIL_SIZE = (80, 80)
    IMAGE_FRAME_FILE = 'img/core/frame.png'
    DEFAULT_ICON_FILE = 'img/core/document.png'
    FILE_UPLOAD_DIRECTORY = 'img/pages'
    THUMBNAIL_UPLOAD_DIRECTORY = 'img/thumbnails'

    title = models.CharField(max_length=64)
    item = models.FileField(upload_to=FILE_UPLOAD_DIRECTORY,
        verbose_name='file')
    uploaded_at = models.DateTimeField(default=datetime.datetime.now,
        editable=False, verbose_name='date uploaded')
    updated_at = models.DateTimeField(auto_now=True, editable=False,
        verbose_name='date updated')
    is_visible = models.BooleanField(default=True, verbose_name="visible")
    thumbnail = models.ImageField(upload_to=THUMBNAIL_UPLOAD_DIRECTORY,
        editable=False)

    objects = FileManager()

    class Meta:
        get_latest_by = 'uploaded_at'
        ordering = ('-uploaded_at', 'title',)
        permissions = (('can_use', 'Can use files'),)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        """
        Save a thumbnail for the uploaded file.  If it's an image the
        thumbnail contains a crop of the image itself, framed within a
        pretty border.  Any file other than an image just gets a default
        icon.
        """
        # The file model object needs to be saved first before the file 
        # itself can be accessed.
        super(File, self).save(force_insert, force_update)
        # If the uploaded file is an image, create a thumbnail based on
        # the image itself.  If it's not an image, use the default
        # thumbnail.
        try:
            # Open the uploaded image and create a thumbnail.
            im = Image.open(self.item.path)
            thumbnail_image = create_thumbnail(im, File.THUMBNAIL_SIZE)
            thumbnail_basename = "%d.png" % self.id
            # Create a new image the same size as the frame image, with
            # the thumbnail centred within it.
            image_frame = Image.open(os.path.join(settings.MEDIA_ROOT,
                File.IMAGE_FRAME_FILE))
            thumbnail_layer = Image.new('RGBA', image_frame.size)
            vertical_pos = (image_frame.size[0] - thumbnail_image.size[0]) / 2
            horizontal_pos = (image_frame.size[1] - thumbnail_image.size[1]) / 2
            thumbnail_layer.paste(thumbnail_image, (vertical_pos,
                horizontal_pos))
            # Layer the thumbnail underneath the frame image.
            thumbnail = Image.composite(image_frame, thumbnail_layer,
                image_frame)
            thumbnail.save(os.path.join(settings.MEDIA_ROOT,
                File.THUMBNAIL_UPLOAD_DIRECTORY, thumbnail_basename),
                format="PNG", optimize=True)
            self.thumbnail = os.path.join(File.THUMBNAIL_UPLOAD_DIRECTORY,
                thumbnail_basename)
        except IOError:
            # The uploaded file isn't an image format supported by PIL.
            self.thumbnail = File.DEFAULT_ICON_FILE
        super(File, self).save(force_insert, force_update)

    def get_absolute_url(self):
        return self.item.url

    def thumbnail_html(self):
        """Return an XHTML image element for the file's thumbnail."""
        im = Image.open(self.thumbnail.path)
        return '<img alt="%s" height="%s" src="%s" width="%s" />' % (
            escape(self.title), im.size[1], escape(self.thumbnail.url),
            im.size[0])
    thumbnail_html.short_description = 'Thumbnail'
    thumbnail_html.allow_tags = True

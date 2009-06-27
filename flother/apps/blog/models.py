import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import permalink

from flother.apps.blog.managers import EntryManager


class Entry(models.Model):

    """An individual entry in the blog."""

    DRAFT_STATUS = 1
    PUBLISHED_STATUS = 2
    STATUS_CHOICES = ((DRAFT_STATUS, 'Draft'), (PUBLISHED_STATUS, 'Published'))

    title = models.CharField(max_length=128)
    slug = models.SlugField(unique_for_year='created_at')
    standfirst = models.CharField(max_length=256, blank=True)
    copy = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    number_of_views = models.PositiveIntegerField(default=0, editable=False)
    status = models.SmallIntegerField(choices=STATUS_CHOICES,
        default=DRAFT_STATUS)

    objects = EntryManager()

    class Meta:
        get_latest_by = 'published_at'
        ordering = ('-published_at',)
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        """Return the canonical URL for a blog entry."""
        from flother.apps.blog.views import entry_detail
        return (entry_detail, (self.created_at.year, self.slug))

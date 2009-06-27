import datetime
from django.db.models import Manager


class EntryManager(Manager):

    """
    Django model manager for the Entry model. Overrides the default
    latest() method so it returns the latest published entry, and adds a
    published() method that returns only published entries.
    """

    def latest(self, field_name=None):
        """Return the latest published entry."""
        return self.published().latest(field_name)

    def published(self, **kwargs):
        """
        Return a QuerySet that contains only those entries deemed fit
        to publish, i.e. entries with a status of "published" and a
        created_at date earlier than now.
        """
        from flother.apps.blog.models import Entry
        return self.get_query_set().filter(status=Entry.PUBLISHED_STATUS,
            published_at__lte=datetime.datetime.now, **kwargs)

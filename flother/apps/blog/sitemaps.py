from django.contrib.sitemaps import Sitemap

from flother.apps.blog.models import Entry


class EntrySitemap(Sitemap):
    """Sitemap for the blog's Entry model."""

    def items(self):
        """Return the Entry objects to appear in the sitemap."""
        return Entry.objects.published()

    def lastmod(self, obj):
        """Return the last modified date for a given Entry object."""
        return obj.updated_at

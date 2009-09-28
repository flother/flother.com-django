from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from staticgenerator import quick_delete


def delete_blog_index(sender, instance, **kwargs):
    """
    Delete all files in the StaticGenerator cache that will be
    out-of-date after a blog entry is saved.  These are:

      * Blog index
      * Archive page for the year the entry was published
      * Admin users' preview page
      * Blog Atom 1.0 feed
      * Page for the blog entry itself
      * Previously published entry's page
      * Next published entry's page
    """
    stagnant_cache_urls = [
        reverse('blog_entry_index'),
        reverse('blog_entry_archive_year', args=[instance.published_at.year]),
        reverse('blog_entry_preview', args=[instance.published_at.year,
            instance.slug]),
        reverse('blog_feeds', args=['latest']),
        instance.get_absolute_url(),
    ]
    try:
        stagnant_cache_urls.append(instance.get_next_published_entry())
    except ObjectDoesNotExist:
        pass
    try:
        stagnant_cache_urls.append(instance.get_previous_published_entry())
    except ObjectDoesNotExist:
        pass
    quick_delete(*stagnant_cache_urls)

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from staticgenerator import quick_delete


def delete_blog_index(sender, instance, **kwargs):
    """
    Delete all files in the StaticGenerator cache that will be
    out-of-date after a blog entry is saved.  These are:

      * About page (it has links to the three most-recent entries)
      * Blog index
      * Archive page for the year the entry was published
      * Admin users' preview page
      * Blog Atom 1.0 feed
      * Page for the blog entry itself
      * Previously published entry's page
      * Next published entry's page
    """
    stagnant_cache_urls = [
        '/about/',
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


def clear_stagnant_cache_on_comment_change(sender, instance, **kwargs):
    """
    Delete the files in the StaticGenerator cache that will be
    out-of-date after a comment is saved or deleted.  These are:

      * Blog index (if this is dealing with the most recent entry)
      * Blog entry page

    Note however that if this is a new comment marked as spam (i.e. the
    ``is_public`` field is False) the cache will not be deleted
    """
    created = kwargs.get('created', False)
    if (not created) or (created and instance.is_public):
        stagnant_cache_urls = [instance.content_object.get_absolute_url()]
        try:
            instance.content_object.get_next_published_entry()
        except ObjectDoesNotExist:
            # This is the most recent entry in the blog so the blog
            # index will need to be removed from the cache.
            stagnant_cache_urls.append(reverse('blog_entry_index'))
        quick_delete(*stagnant_cache_urls)

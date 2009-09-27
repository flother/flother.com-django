from django.core.urlresolvers import reverse
from staticgenerator import quick_delete


def delete_blog_index(sender, instance, **kwargs):
    stagnant_cache_urls = (
        reverse('blog_entry_index'),
        reverse('blog_entry_archive_year', args=[instance.published_at.year]),
        reverse('blog_entry_detail', args=[instance.published_at.year,
            instance.slug]),
        reverse('blog_entry_preview', args=[instance.published_at.year,
            instance.slug]),
        reverse('blog_feeds', args=['latest']),
    )
    quick_delete(*stagnant_cache_urls)

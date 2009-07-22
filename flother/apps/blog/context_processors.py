from flother.apps.blog.models import Entry


def latest_entries(request):
    """Return the three latest published entries."""
    return {
        'latest_entries': Entry.objects.published()[:3]
    }

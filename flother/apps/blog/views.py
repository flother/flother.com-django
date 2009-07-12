from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext

from flother.apps.blog.models import Entry


def entry_index(request):
    """Output the latest ten published blog entries."""
    latest_entry = Entry.objects.latest()
    recent_entries = Entry.objects.published().exclude(id=latest_entry.id)[:10]
    years_with_entries = Entry.objects.published().dates('published_at', 'year')
    context = {
        'latest_entry': latest_entry,
        'recent_entries': recent_entries,
        'years_with_entries': years_with_entries,
    }
    return render_to_response('blog/entry_index.html', context,
        RequestContext(request))


def entry_archive_year(request, year):
    """Output the published blog entries for a given year."""
    entries = get_list_or_404(Entry.objects.published(), published_at__year=year)

    entries_by_month = dict.fromkeys(range(1, 13), 0)
    for entry in entries:
        entries_by_month[entry.published_at.month] += 1
    context = {
        'year': year,
        'entries': entries,
        'entries_by_month': entries_by_month,
        'max_entries_per_month': max(entries_by_month.values()),
    }
    return render_to_response('blog/entry_archive_year.html', context,
        RequestContext(request))


def entry_detail(request, year, slug):
    """
    Output a full individual entry; this is the view for an entry's
    permalink.
    """
    entry = get_object_or_404(Entry.objects.published(), published_at__year=year,
        slug=slug)
    if not request.user.is_staff:
        entry.number_of_views += 1
        entry.save()
    context = {'entry': entry}
    return render_to_response('blog/entry_detail.html', context,
        RequestContext(request))

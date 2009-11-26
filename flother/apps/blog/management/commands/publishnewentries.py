import datetime

from django.core.management.base import NoArgsCommand

from flother.apps.blog.models import Entry
from flother.apps.blog.signals import delete_blog_index


class Command(NoArgsCommand):

  """
  Because the site is heavily cached (it's served as static HTML files),
  any entry published in the future will only actually appear once the
  cache is flushed, not once its publishing date has passed.  To ensure
  the entry appears as expected, this command will check for entries
  whose ``published_at`` field is within the last hour.  If there are any,
  the cache will be cleared.

  This command should be run as an hourly cron job.
  """

  help = "Clears the cache if any entries were published within the last hour."

  def handle_noargs(self, **options):
    """
    Delete the cache for any blog entries published within the last hour.
    """
    verbosity = int(options.get('verbosity', 1))

    one_hour_ago = datetime.datetime.now() - datetime.timedelta(minutes=62)
    if verbosity == 2:
      print "Looking for entries published before %s." % one_hour_ago.strftime('%H:%M:%S on %d %B %Y')
    new_entries = Entry.objects.published(published_at__gte=one_hour_ago)
    if verbosity == 2:
      print "Found %d entries." % len(new_entries)

    if new_entries:
      for entry in new_entries:
        if verbosity >= 1:
          print "Deleting cache for entry '%s'." % entry.title
        delete_blog_index(Entry, entry)

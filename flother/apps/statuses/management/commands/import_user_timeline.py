"""
Django management command to import messages from Twitter for one
particular user.  The Twitter username is defined as ``TWITTER_USERNAME``
in the project's settings and is mapped to a database user using the
``TWITTER_USER_MAPPING`` setting, e.g.:

  TWITTER_USERNAME = "riggbot"
  TWITTER_USER_MAPPING = {
    "riggbot": "matt",
  }

The value for ``TWITTER_USER_MAPPING["riggbot"]``, ``matt``, is the
username for the database user you want to assign the Twitter messages to.

Run the command as you would any Django management command:

  django-admin.py import_user_timeline

There are no command-line options, other than Django's defaults.

Note that because Twitter's API is (currently) limited to 75 calls in one
hour, if there are more than 6,000 messages to retrieve this import will
get the most recent 6,000 messages and the raise an error.

If you need to import more than 6,000 messages you'll need to change the
``MESSAGES_PER_PAGE`` setting (to a maximum of 200; if you need to import
more than 15,000 messages you're on your own.)
"""
import datetime

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.contrib.auth.models import User
import twitter

from flother.apps.statuses.models import Status


MESSAGES_PER_PAGE = 80


def create_datetime_from_string(date_string):
    """
    Return a ``datetime.datetime`` object from the given string, which
    must be in the format ``"%a %b %d %H:%M:%S +0000 %Y"``.
    """
    # There seems to be an issue using %z for the time-zone information, so
    # this is a little naive.  See http://bugs.python.org/issue6641.
    return datetime.datetime.strptime(date_string, "%a %b %d %H:%M:%S +0000 %Y")


def log(message, verbosity):
    """Print a message to the console if the verbosity level is 2."""
    if verbosity == 2:
        print message


class Command(NoArgsCommand):

    help = "Saves new public messages posted by the Twitter user specified in settings.TWITTER_USERNAME."

    def handle_noargs(self, **options):
        """
        Saves new public messages posted by the Twitter user specified in
        ``settings.TWITTER_USERNAME``.
        """
        verbosity = int(options.get('verbosity', 1))
        api = twitter.Api()
        # Get the database user to which to link new messages.
        user = User.objects.get(username=settings.TWITTER_USER_MAPPING[settings.TWITTER_USERNAME])
        # Find the second-most recent message stored in the database and use it
        # to limit Twitter's responses to only newer messages.  That way, once
        # a duplicate is found (the *most* recent message) we'll know a copy of
        # every message has been taken. If there are no messages in the
        # database, set no limit to Twitter's responses.
        try:
            last_message = Status.objects.all().order_by("-created_at")[1]
            log("Looking for messages before %s." % last_message.created_at,
                verbosity)
        except IndexError:
            # No messages yet stored in the database.
            last_message = None
            log("Looking for all messages.", verbosity)
        new_messages = 0
        page = 1
        last_message_found = False
        # Keep requesting pages from Twitter until the most recent message in
        # the database is returned.
        while not last_message_found:
            log("Requesting page %d." % page, verbosity)
            # Here's the actual call to Twitter.
            statuses = api.GetUserTimeline(settings.TWITTER_USERNAME,
                since_id=getattr(last_message, "id", None), page=page,
                count=MESSAGES_PER_PAGE)
            if len(statuses) == 0:
                last_message_found = True
                log("Come to the end of the user's messages.", verbosity)
            # Save each message sent by Twitter.
            for s in statuses:
                try:
                    Status.objects.get(remote_id=s.id)
                    # A duplicate message is assumed to be the last new message
                    # from the previous import.
                    log("Found duplicate message; finishing import.", verbosity)
                    last_message_found = True
                    break
                except Status.DoesNotExist:
                    status = Status(remote_id=s.id, user=user,
                        screen_name=s.user.screen_name, text=s.text,
                        source=s.source, in_reply_to_id=s.in_reply_to_status_id,
                        created_at=create_datetime_from_string(s.created_at))
                    status.save()
                    new_messages = new_messages + 1
            page = page + 1
        log("Import complete; %d new messages saved." % new_messages, verbosity)

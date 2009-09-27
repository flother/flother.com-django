import datetime
import unicodedata
import urllib2

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator
from django.core.mail import mail_managers
from django.db import models
from django.db.models import permalink
from django.template.loader import render_to_string

from flother.apps.blog.managers import EntryManager
from flother.utils.akismet import Akismet


class Entry(models.Model):

    """An individual entry in the blog."""

    DRAFT_STATUS = 1
    PUBLISHED_STATUS = 2
    PRIVATE_STATUS = 3
    STATUS_CHOICES = ((DRAFT_STATUS, 'Draft'), (PUBLISHED_STATUS, 'Published'),
        (PRIVATE_STATUS, 'Private'))

    DAYS_COMMENTS_ENABLED = 300

    title = models.CharField(max_length=128)
    slug = models.SlugField(unique_for_year='published_at')
    standfirst = models.CharField(max_length=256, blank=True)
    copy = models.TextField()
    copy_html = models.TextField(blank=True)
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name='date_created')
    published_at = models.DateTimeField(default=datetime.datetime.now,
        verbose_name='date published')
    updated_at = models.DateTimeField(auto_now=True,
        verbose_name='date updated')
    number_of_views = models.PositiveIntegerField(default=0, editable=False)
    status = models.SmallIntegerField(choices=STATUS_CHOICES,
        default=DRAFT_STATUS)
    enable_comments = models.BooleanField(default=False)

    objects = EntryManager()

    class Meta:
        get_latest_by = 'published_at'
        ordering = ('-published_at',)
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        """
        Use Markdown to convert the ``copy`` field from plain-text to
        HTMl.  Smartypants is also used to bring in curly quotes.
        """
        from markdown import markdown
        from smartypants import smartyPants
        self.copy_html = smartyPants(markdown(self.copy, ['abbr',
            'headerid(level=2)']))
        super(Entry, self).save(force_insert=False, force_update=False)

    @permalink
    def get_absolute_url(self):
        """Return the canonical URL for a blog entry."""
        from flother.apps.blog.views import entry_detail
        return (entry_detail, (self.published_at.year, self.slug))

    def allow_new_comment(self):
        """
        Return True if a new comment can be posted for this entry,
        False otherwise.  Comments can be posted if the the final date
        for comments has not yet been reached.
        """
        date_for_comments = self.published_at + datetime.timedelta(
            days=Entry.DAYS_COMMENTS_ENABLED)
        return bool(self.enable_comments and (datetime.datetime.now() <=
            date_for_comments))

    def get_previous_published_entry(self):
        """
        Return the previous public entry published before the current
        time and date.
        """
        return self.get_previous_by_published_at(status=self.PUBLISHED_STATUS,
            published_at__lte=datetime.datetime.now)

    def get_next_published_entry(self):
        """
        Return the next public entry published before the current time
        and date.
        """
        return self.get_next_by_published_at(status=self.PUBLISHED_STATUS,
            published_at__lte=datetime.datetime.now)


class EntryModerator(CommentModerator):

    """
    Comment moderation for the Entry model.  An email is sent once a
    comment is submitted.  Comments are automatically rejected sixty
    days after the blog post was published.
    """

    auto_close_field = 'published_at'
    close_after = Entry.DAYS_COMMENTS_ENABLED
    email_notification = True

    def allow(self, comment, content_object, request):
        """
        Only allow the comment if the entry's ``enable_comments`` field
        is set to True and the entry is published (i.e. not draft or
        private).
        """
        return (content_object.enable_comments and
            content_object.status == Entry.PUBLISHED_STATUS)

    def moderate(self, comment, content_object, request):
        """
        Return True or False, True indicating that the Akismet
        spam-checking service thinks the comment is spam.  As the
        Akismet library doesn't handle Unicode all user-input is
        converted to ASCII before it's passed to the library.
        """
        api = Akismet(key=settings.AKISMET_API_KEY)
        for k in comment.userinfo:
            comment.userinfo[k] = unicodedata.normalize('NFKD',
                comment.userinfo[k]).encode('ascii', 'ignore')
        comment_data = {
            'user_ip': comment.ip_address,
            'user_agent': '',
            'comment_author': comment.userinfo['name'],
            'comment_author_url': comment.userinfo['url'],
            'permalink': comment.get_absolute_url(),
        }
        try:
            return api.comment_check(unicodedata.normalize('NFKD',
                comment.comment).encode('ascii', 'ignore'), comment_data)
        except (urllib2.HTTPError, urllib2.URLError):
            # If Akismet is down the safest option is to assume the
            # comment needs moderating.
            return True

    def email(self, comment, content_object, request):
        """
        Email the details of the newly-submitted comment to the site
        managers.  An email is only sent if the comments ``is_public``
        field is set to True (i.e. not spam).
        """
        if comment.is_public:
            context = {
                'comment': comment,
                'entry': content_object,
            }
            email_body = render_to_string('blog/new_comment_email.txt', context)
            mail_managers(u'Comment on "%s"' % content_object, email_body)


moderator.register(Entry, EntryModerator)

import datetime

from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator
from django.core.mail import mail_managers
from django.db import models
from django.db.models import permalink
from django.template.loader import render_to_string

from flother.apps.blog.managers import EntryManager


class Entry(models.Model):

    """An individual entry in the blog."""

    DRAFT_STATUS = 1
    PUBLISHED_STATUS = 2
    PRIVATE_STATUS = 3
    STATUS_CHOICES = ((DRAFT_STATUS, 'Draft'), (PUBLISHED_STATUS, 'Published'),
        (PRIVATE_STATUS, 'Private'))

    DAYS_COMMENTS_ENABLED = 60

    title = models.CharField(max_length=128)
    slug = models.SlugField(unique_for_year='published_at')
    standfirst = models.CharField(max_length=256, blank=True)
    copy = models.TextField()
    author = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
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


class EntryModerator(CommentModerator):

    """
    Comment moderation for the Entry model.  An email is sent once a
    comment is submitted.  Comments are automatically rejected sixty
    days after the blog post was published.
    """

    auto_close_field = 'published_at'
    close_after = Entry.DAYS_COMMENTS_ENABLED
    email_notification = True
    enable_field = 'enable_comments'

    def email(self, comment, content_object, request):
        """
        Email the details of the newly-submitted comment to the site
        managers.
        """
        context = {
            'comment': comment,
            'entry': content_object,
        }
        email_body = render_to_string('blog/new_comment_email.txt', context)
        mail_managers(u'New comment on %s' % content_object, email_body)

moderator.register(Entry, EntryModerator)

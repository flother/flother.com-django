from django.db import models
from django.utils.text import truncate_words


class Message(models.Model):

    """A message sent to me through the web site."""

    sender_name = models.CharField(max_length=64)
    sender_email = models.EmailField()
    body = models.TextField()
    is_spam = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name='date sent')
    updated_at = models.DateTimeField(auto_now=True,
        verbose_name='date updated')

    class Meta:
        get_latest_by = 'created_at'
        ordering = ('-created_at',)

    def __unicode__(self):
        return u'%s: %s' % (self.sender_name, self.body_teaser())

    def body_teaser(self):
        return truncate_words(self.body, 10)
    body_teaser.short_description = 'body'
    
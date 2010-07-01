from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):

    """A simple representation of a Twitter message."""

    remote_id = models.CharField(max_length=8, unique=True)
    user = models.ForeignKey(User)
    screen_name = models.CharField(max_length=20)
    text = models.CharField(max_length=140)
    source = models.CharField(max_length=128)
    in_reply_to_id = models.CharField(max_length=8, blank=True, null=True,
        verbose_name="in reply to")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "created_at"
        ordering = ("-created_at",)
        unique_together = (("text", "created_at"),)
        verbose_name_plural = "statuses"

    def __unicode__(self):
        return self.text

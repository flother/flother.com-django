import time

from django.contrib.comments.forms import CommentForm
from django import forms
from django.forms.util import ErrorDict


class CommentFormForCaching(CommentForm):

    """
    Django's CommentForm class minus the security fields.

    Because the site is heavily cached the security fields won't work
    as they're based on a timestamp that will go out-of-date very
    quickly on a cached page.
    """

    def clean_timestamp(self):
        """
        Return the timestamp without throwing an error.  Because blog
        entries are heavily cached the forms timestamp will be
        out-of-date almost all the time, so there's no point in
        checking.  Akismet can handle spam.
        """
        return self.cleaned_data["timestamp"]

    def security_errors(self):
        """Return just those errors associated with security."""
        errors = ErrorDict()
        if 'honeypot' in self.errors:
            errors['honeypot'] = self.errors['honeypot']
        return errors

    def generate_security_hash(self, content_type, object_pk, timestamp):
        """Generate a SHA1 security hash."""
        return 'ce7501007f04a6529e650f1f1b3fc0586d1d94eb'

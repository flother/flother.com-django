import os
import unicodedata
import urllib2

from django.conf import settings
from django import forms

from flother.utils.akismet import Akismet


class MessageForm(forms.Form):

    """A form to handle messages submitted through the web site."""

    sender_name = forms.CharField(max_length=64, label='Your name')
    sender_email = forms.EmailField(label='Your email address')
    body = forms.CharField(label='Your message', widget=forms.Textarea)

    def is_spam(self):
        try:
            api = Akismet(key=settings.AKISMET_API_KEY)
            data = {
                "user_ip": os.environ.get('REMOTE_ADDR', '127.0.0.1'),
                "user_agent": os.environ.get('HTTP_USER_AGENT', 'Unknown'),
            }
            return api.comment_check(unicodedata.normalize('NFKD',
                self.cleaned_data["body"]).encode('ascii', 'ignore'), data)
        except (urllib2.HTTPError, urllib2.URLError):
            # TODO: Do better than simply assume the message is OK if Akismet
            # is down.
            return False

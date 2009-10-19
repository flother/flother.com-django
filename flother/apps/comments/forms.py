import time

from django.contrib.comments.forms import CommentForm
from django import forms
from django.forms.util import ErrorDict


class CommentFormForCaching(CommentForm):
    def security_errors(self):
        errors = ErrorDict()
        if 'honeypot' in self.errors:
            errors['honeypot'] = self.errors['honeypot']
        return errors

    def initial_security_hash(self, timestamp):
        return ''

    def generate_security_hash(self, content_type, object_pk, timestamp):
        return ''
from django import template
from django.conf import settings
from django.utils.html import escape
from django.utils.hashcompat import md5_constructor


register = template.Library()


DEFAULT_GRAVATAR_IMAGE = '%simg/core/avatar.png' % settings.MEDIA_URL
GRAVATAR_RATING = 'r'


@register.simple_tag
def gravatarimg(email, size=32):
    email_hash = md5_constructor(email).hexdigest()
    url = 'http://www.gravatar.com/avatar/%s?s=%d&r=%s&d=%s' % (email_hash,
        size, GRAVATAR_RATING, DEFAULT_GRAVATAR_IMAGE)
    return '<img alt="Gravatar" height="%s" src="%s" width="%s" />' % (size,
        escape(url), size)

import re

from django import template
from django.conf import settings
from django.utils.html import escape
from django.utils.hashcompat import md5_constructor


register = template.Library()


DEFAULT_GRAVATAR_IMAGE = '%score/img/avatar.png' % settings.MEDIA_URL
GRAVATAR_RATING = 'r'
PULLQUOTE_RE = re.compile(r'<blockquote\sclass="pullquote">.+?</blockquote>',
    re.UNICODE)


@register.simple_tag
def gravatarimg(email, size=32):
    email_hash = md5_constructor(email).hexdigest()
    url = 'http://www.gravatar.com/avatar/%s?s=%d&r=%s&d=%s' % (email_hash,
        size, GRAVATAR_RATING, DEFAULT_GRAVATAR_IMAGE)
    return '<img alt="Gravatar" height="%s" src="%s" width="%s" />' % (size,
        escape(url), size)


@register.filter
def strip_pullquotes(copy):
    """
    Strip pullquotes from the given blog entry copy.  This is used
    in the Atom feed template, as the pullquotes are confusing and out
    of place without CSS applied.

    As an example, given the string::

    >>> s = '<p>Lorem <a href="#">ipsum</a>.</p><blockquote class="pullquote"><p>Dolor sit amet</p></blockquote><p>consectetur adipisicing elit</p>'
    >>> strip_pullquotes(s)
    '<p>Lorem <a href="#">ipsum</a>.</p><p>consectetur adipisicing elit</p>'
    >>> s = '<blockquote><p>Lorem ipsum</p></blockquote><blockquote class="pullquote"><p>Dolor sit amet</p></blockquote><blockquote><p>consectetur adipisicing elit</p></blockquote>'
    >>> strip_pullquotes(s)
    '<blockquote><p>Lorem ipsum</p></blockquote><blockquote><p>consectetur adipisicing elit</p></blockquote>'
    """
    return PULLQUOTE_RE.sub('', copy)

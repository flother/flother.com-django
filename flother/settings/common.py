import os
import sys


SITE_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = False
DATE_FORMAT = 'l, jS F Y'
TIME_FORMAT = 'P'
DATETIME_FORMAT = ', '.join([TIME_FORMAT, DATE_FORMAT])
MONTH_DAY_FORMAT = 'j F'

ROOT_URLCONF = 'flother.urls'

SEND_BROKEN_LINK_EMAILS = True

COMMENTS_HIDE_REMOVED = False

SOUTH_AUTO_FREEZE_APP = True

COMPRESS_VERSION = True
COMPRESS_AUTO = False
COMPRESS_CSS = {
    'flother': {
        'source_filenames': ('core/css/reset.css', 'core/css/structure.css',
            'core/css/typography.css', 'core/css/sections.css'),
        'output_filename': 'core/css/flother.r?.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}
COMPRESS_JS = {}
CSSTIDY_ARGUMENTS = '--preserve_css=true --remove_last_\;=true --lowercase_s=true --sort_properties=true --template=highest'

STATIC_GENERATOR_URLS = (
    r'^/(blog|about)',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'flother.apps.blog.context_processors.latest_entries',
    'flother.utils.context_processors.section',
    'flother.utils.context_processors.current_year',
)
TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
 
MIDDLEWARE_CLASSES = (
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'staticgenerator.middleware.StaticGeneratorMiddleware',
    'flother.utils.middleware.http.SetRemoteAddrFromForwardedFor',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.redirects',

    'south',
    'compress',
    'participationgraphs',
    'typogrify',

    'flother.apps.blog',
    'flother.apps.comments',
    'flother.apps.photos',
    'flother.apps.files',
    'flother.apps.contact',
    'flother.apps.search',
)

COMMENTS_APP = 'flother.apps.comments'

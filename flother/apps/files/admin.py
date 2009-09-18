from django.contrib import admin

from flother.apps.files.models import File


class FileAdmin(admin.ModelAdmin):

    """
    Class for specifiying the options for administering the
    flother.apps.blog.models.File model via the Django admin.
    """

    date_hierarchy = 'uploaded_at'
    list_display = ('thumbnail_html', 'title', 'uploaded_at', 'is_visible')
    list_display_links = ('thumbnail_html', 'title')
    list_filter = ('uploaded_at', 'is_visible',)
    search_fields = ('title',)

admin.site.register(File, FileAdmin)

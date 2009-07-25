from django.contrib import admin

from flother.apps.blog.models import Entry


class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'published_at'
    list_display = ('title', 'author', 'published_at', 'number_of_views',
        'status')
    list_filter = ('author', 'status')
    prepopulated_fields = {'slug': ('title',)}
    radio_fields = {'status': admin.HORIZONTAL}
    search_fields = ('title', 'standfirst', 'copy')


admin.site.register(Entry, EntryAdmin)

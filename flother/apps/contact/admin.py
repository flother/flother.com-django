from django.contrib import admin
from flother.apps.contact.models import Message


class MessageAdmin(admin.ModelAdmin):
    actions = None
    date_hierarchy = 'created_at'
    list_display = ['sender_name', 'sender_email', 'body_teaser', 'created_at',
        'is_spam']
    list_filter = ['is_spam']
    search_fields = ['sender_name', 'sender_email', 'body']

admin.site.register(Message, MessageAdmin)

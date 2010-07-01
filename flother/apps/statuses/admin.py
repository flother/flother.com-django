from django.contrib import admin

from flother.apps.statuses.models import Status


class StatusAdmin(admin.ModelAdmin):
    exclude = ("remote_id",)
    fieldsets = (
        (None, {
            "fields": (("user", "screen_name", "in_reply_to_id"), "text",
                "source", "created_at")
        }),
    )
    date_hierarchy = 'created_at'
    list_display = ("text", "created_at")
    search_fields = ('text',)


admin.site.register(Status, StatusAdmin)

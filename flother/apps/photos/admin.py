from django.contrib import admin

from flother.apps.photos import models


class PhotoAdmin(admin.ModelAdmin):

    """Django model admin for ``flother.apps.photos.models.Photo``."""

    date_hierarchy = 'taken_at'
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'original', 'photographer', 'description'
            )
        }),
        ('Metadata', {
            'fields': (
                'taken_at', 'point', 'exposure', 'aperture', 'focal_length',
                'iso_speed', 'status', 'camera'
            )
        }),
        ('Relationships', {
            'fields': (
                'collections',
            ),
            'classes': (
                'collapse',
            )
        }),
    )
    filter_horizontal = ('collections',)
    list_display = ('thumbnail_html', 'title', 'photographer', 'taken_at',
        'location', 'status')
    list_display_links = ('thumbnail_html', 'title')
    list_filter = ('photographer', 'status', 'camera')
    prepopulated_fields = {'slug': ('title',)}
    radio_fields = {'status': admin.HORIZONTAL}
    search_fields = ('title', 'description', 'exposure', 'aperture',
        'focal_length', 'iso_speed')

    def queryset(self, request):
        if request.user.is_superuser:
            return models.Photo.objects.all()
        return models.Photo.objects.filter(photographer=request.user)


class CollectionAdmin(admin.ModelAdmin):

    """Django model admin for ``flother.apps.photos.models.Collection``."""

    exclude = ('description_html', 'created_at', 'updated_at')
    list_display = ('title', 'number_of_photos')
    list_select_related = True
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


class PointAdmin(admin.ModelAdmin):

    """Django model admin for ``flother.apps.photos.models.Point``."""

    fieldsets = ((None, {'fields': (('longitude', 'latitude'), 'location')}),)
    list_display = ('__unicode__', 'longitude', 'latitude', 'location',
        'number_of_photos')
    list_editable = ('longitude', 'latitude', 'location',)
    list_select_related = True
    list_filter = ('location',)


class LocationAdmin(admin.ModelAdmin):

    """Django model admin for ``flother.apps.photos.models.Location``."""

    list_display = ('name', 'country', 'number_of_photos')
    list_filter = ('country',)
    list_select_related = True
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class CountryAdmin(admin.ModelAdmin):

    """Django model admin for ``flother.apps.photos.models.Country``."""

    list_display = ('name', 'formal_name', 'country_code', 'number_of_photos')
    list_editable = ('formal_name',)
    list_select_related = True
    search_fields = ('name', 'formal_name')


class CameraAdmin(admin.ModelAdmin):

    """Django model admin for ``flother.apps.photos.models.Camera``."""

    exclude = ('description_html',)
    list_display = ('name', 'number_of_photos')
    list_select_related = True
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


admin.site.register(models.Photo, PhotoAdmin)
admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Point, PointAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.Camera, CameraAdmin)

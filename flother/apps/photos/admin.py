from django.contrib import admin

from flother.apps.photos import models


class PhotoAdmin(admin.ModelAdmin):
    date_hierarchy = 'taken_at'
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'original', 'photographer',
            'description')}),
        ('Metadata', {'fields': ('taken_at', 'point', 'exposure', 'aperture',
            'focal_length', 'iso_speed', 'status', 'camera', ('collections', 'people')), 'classes': ('collapse',)}),
    )
    # filter_horizontal / filter_vertical ?
    list_display = ('thumbnail_html', 'title', 'photographer', 'taken_at', 'location', 'status')
    list_display_links = ('thumbnail_html', 'title')
    list_filter = ('photographer', 'status')
    prepopulated_fields = {'slug': ('title',)}
    radio_fields = {'status': admin.HORIZONTAL}
    search_fields = ('title', 'description', 'exposure', 'aperture',
        'focal_length', 'iso_speed')

    def queryset(self, request):
        if request.user.is_superuser:
            return models.Photo.objects.all()
        return models.Photo.objects.filter(photographer=request.user)


class CollectionAdmin(admin.ModelAdmin):
    pass


class PointAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('longitude', 'latitude'), 'location')}),)
    list_display = ('location', 'longitude', 'latitude')
    list_filter = ('location',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'country_code', 'long_name', 'formal_name')
    list_editable = ('country_code', 'long_name', 'formal_name')
    search_fields = ('short_name', 'long_name', 'formal_name')


class CameraAdmin(admin.ModelAdmin):
    pass


class PersonAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Photo, PhotoAdmin)
admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Point, PointAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.Camera, CameraAdmin)
admin.site.register(models.Person, PersonAdmin)

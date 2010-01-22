from django.contrib import admin

from flother.apps.places import models


class PointAdmin(admin.ModelAdmin):

    """Django model admin for ``flother.apps.places.models.Point``."""

    fieldsets = ((None, {'fields': (('longitude', 'latitude'), 'location')}),)
    list_display = ('__unicode__', 'longitude', 'latitude', 'location',
        'number_of_photos')
    list_editable = ('longitude', 'latitude', 'location',)
    list_select_related = True
    list_filter = ('location',)


class LocationAdmin(admin.ModelAdmin):

    """Django model admin for ``flother.apps.places.models.Location``."""

    list_display = ('name', 'country', 'number_of_photos')
    list_filter = ('country',)
    list_select_related = True
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class CountryAdmin(admin.ModelAdmin):

    """Django model admin for ``flother.apps.places.models.Country``."""

    list_display = ('name', 'formal_name', 'country_code', 'number_of_photos')
    list_editable = ('formal_name',)
    list_select_related = True
    search_fields = ('name', 'formal_name')


admin.site.register(models.Point, PointAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Country, CountryAdmin)

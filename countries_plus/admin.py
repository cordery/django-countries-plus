from django.contrib import admin

from .models import Country


class CountryAdmin(admin.ModelAdmin):
    list_display = ('continent', 'name', 'iso', 'iso3', 'languages', 'currency_name')
    list_display_links = ('name',)
    search_fields = ('name', 'iso', 'iso3')
    """Provided so that other ModelAdmins that have """
    list_filter = ('continent',)


admin.site.register(Country, CountryAdmin)

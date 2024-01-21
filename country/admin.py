from django.contrib import admin

from core.admin import CustomModelAdmin
from country.models import Country


class CountryAdmin(CustomModelAdmin):
    list_display = ["title", "iso3", "currency", "phone_code"]


admin.site.register(Country, CountryAdmin)

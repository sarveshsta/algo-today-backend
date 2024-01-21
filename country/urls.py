from django.urls import path

from country.views import CountryListView

app_name = "country"

urlpatterns = [
    path("", CountryListView.as_view(), name="country_list"),
]

from django.urls import include, path

app_name = "v1"

urlpatterns = [
    path("country/", include("country.urls")),
    path("users/", include("users.urls")),
]

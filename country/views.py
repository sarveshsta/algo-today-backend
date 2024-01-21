from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from country.models import Country
from country.serializers import CountrySerializers


class CountryListView(ListAPIView):
    """
    Retrieve a paginated list of countries.

    Allows users to retrieve a paginated list of countries with optional search functionality.

    - **HTTP Methods**:
        - **GET**: Retrieve a paginated list of countries.

    - **Query Parameters**:
        - `search`: Perform a case-insensitive search on country titles and phone codes.

    - **Pagination Parameters**:
        - `page`: Specify the page number (default is 1).
        - `page_size`: Specify the number of items per page (default is 10).

    Example:
    ```
    # GET
    /countries/

    # GET with search and pagination
    /countries/?search=united&page=2&page_size=5
    ```

    Response:
    ```
    {
        "count": 150,
        "next": "http://example.com/api/countries/?page=2",
        "previous": "http://example.com/api/countries/",
        "results": [
            {
                "id": 1,
                "title": "United States",
                "flag": "https://example.com/flag-us.png",
                "iso3": "USA",
                "iso2": "US",
                "phone_code": "+1",
                "currency": "USD"
            },
            ...
        ]
    }
    ```
    """

    permission_classes = [AllowAny]
    serializer_class = CountrySerializers
    queryset = Country.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["title", "phone_code"]

from django.conf import settings

from rest_framework import serializers

from core.serializers import BaseModelSerializer
from country.models import Country


class CountrySerializers(BaseModelSerializer):
    """
    Country Serializer
    ------------------

    Serializer for the Country model.

    This serializer is used to convert Country model instances to JSON format and vice versa.
    It includes additional fields and methods for customization.

    Attributes:
        flag (str): A serialized field representing the URL of the country flag. (Method Field)

    Meta:
        model (Country): Reference to the Country model.
        fields (list): List of fields to be included in the serialized output.
        read_only_fields (list): List of fields that should be read-only in the serialized output.

    Methods:
        get_flag: Method to retrieve the complete URL of the country flag.

    Example:
        serializer = CountrySerializer(instance=country_instance)
        serialized_data = serializer.data
    """

    flag = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ["id", "title", "flag", "iso3", "iso2", "phone_code", "currency"]
        read_only_fields = ["id"]

    def get_flag(self, obj):
        if obj.flag:
            return settings.BASE_URL + str(obj.flag)
        return None

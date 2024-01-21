from django.db import models
from django.utils.translation import gettext as _, gettext_lazy as _

from core.models import BaseModel


class Country(BaseModel):
    """
    Country Model
    -------------

    Model to represent information about a country.

    Attributes:
        title (str): The title of the country.
        flag (str): The URL for the country's flag.
        iso3 (str): The three-letter ISO code of the country.
        iso2 (str): The two-letter ISO code of the country.
        phone_code (str): The phone code of the country.
        currency (str): The currency of the country.

    Methods:
        __str__: Returns a string representation of the country.

    Meta:
        verbose_name (str): A human-readable name for the model.
        verbose_name_plural (str): A human-readable plural name for the model.
        db_table (str): The database table name for the model.
        ordering (list of str): The default ordering for the model.

    """

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=150,
        db_column="title",
        unique=True,
        help_text=_("Enter the country title."),
    )
    flag = models.URLField(
        verbose_name=_("Flag"),
        max_length=250,
        db_column="flag",
        help_text=_("Enter the URL for the country flag."),
    )
    iso3 = models.CharField(
        verbose_name=_("ISO Code 3"),
        max_length=10,
        db_column="iso3",
        unique=True,
        help_text=_("Enter the three-letter ISO code."),
    )
    iso2 = models.CharField(
        verbose_name=_("ISO Code 2"),
        max_length=10,
        db_column="iso2",
        unique=True,
        help_text=_("Enter the two-letter ISO code."),
    )
    phone_code = models.CharField(
        verbose_name=_("Phone Code"),
        max_length=5,
        db_column="phone_code",
        help_text=_("Enter the country phone code."),
    )
    currency = models.CharField(
        verbose_name=_("Currency"),
        max_length=20,
        db_column="currency",
        help_text=_("Enter the country currency."),
    )

    def __str__(self):
        """
        Return a string representation of the country.
        """
        return str(self.title)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        db_table = "Country"
        ordering = ["title"]

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..models import Currency, Provider


class Endpoint(models.Model):
    url = models.CharField(max_length=255)
    pattern_block = models.CharField(max_length=255, null=True, blank=True)
    pattern_timestamp = models.CharField(max_length=255, null=True, blank=True)
    header = models.CharField(max_length=255, null=True, blank=True)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="endpoint_currencies"
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT,
        related_name="endpoint_providers"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["currency", "provider"],
                name="unique_currency_provider"
            )
        ]

    def __str__(self):
        return self.url

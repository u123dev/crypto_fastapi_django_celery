from django.db import models
from django.utils.translation import gettext_lazy as _

from ..models import Currency, Provider


class Block(models.Model):
    block_number = models.IntegerField()
    created_at = models.DateTimeField(db_index=True, null=True, blank=True)
    stored_at = models.DateTimeField(db_index=True, auto_now=True)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="block_currencies"
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.PROTECT,
        related_name="block_providers"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["block_number", "currency"],
                name="unique_currency_block_number"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return (f"{self.block_number} - {self.currency} - "
                f"{str(self.provider)} - {self.created_at} - "
                f"{self.stored_at}")

from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    MAX_LENGTH_CURRNAME = 10
    name = models.CharField(max_length=MAX_LENGTH_CURRNAME, unique=True)

    class Meta:
        verbose_name = _("currency")
        verbose_name_plural = _("currencies")
        ordering = ["name"]

    def __str__(self):
        return self.name

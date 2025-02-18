from django.db import models
from django.utils.translation import gettext_lazy as _


class Provider(models.Model):
    name = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

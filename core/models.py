from django.db import models
from django.utils import timezone
from . import managers


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()

    # created = models.DateTimeField(default=timezone.now())
    # updated = models.DateTimeField(default=timezone.now())

    class Meta:
        abstract = True

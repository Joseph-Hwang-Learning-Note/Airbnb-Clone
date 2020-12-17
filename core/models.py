from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # created = models.DateTimeField(default=timezone.now())
    # updated = models.DateTimeField(default=timezone.now())

    class Meta:
        abstract = True

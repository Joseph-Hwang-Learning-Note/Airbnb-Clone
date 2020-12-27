from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core import models as core_models

# Also you can try the way below

# class IntegerRangeField(models.IntegerField):
#     def __init__(
#         self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs
#     ):
#         self.min_value, self.max_value = min_value, max_value
#         models.IntegerField.__init__(self, verbose_name, name, **kwargs)

#     def formfield(self, **kwargs):
#         defaults = {"min_value": self.min_value, "max_value": self.max_value}
#         defaults.update(kwargs)
#         return super(IntegerRangeField, self).formfield(**defaults)


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    Accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Check_in = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="reviews"
    )

    def __str__(self):
        return f"{self.review} - {self.room}"

    def rating_average(self):
        avg = (
            self.Accuracy
            + self.Communication
            + self.Cleanliness
            + self.Location
            + self.Check_in
            + self.Value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "ratings"

    class Meta:
        ordering = ("-created",)

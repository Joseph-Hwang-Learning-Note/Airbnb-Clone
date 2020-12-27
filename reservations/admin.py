from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from . import models


@admin.register(models.Reservation)
class ReservationAdmin(ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "room",
        "check_in",
        "check_out",
        "status",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status",)

    search_fields = (
        "room__name__icontains",
        "guest__username__icontains",
    )


@admin.register(models.BookedDay)
class BookedDayAdmin(ModelAdmin):

    list_display = ("day", "reservation")

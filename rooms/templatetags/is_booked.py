import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag  # If you do takes_context=True, you can get context from every .pys
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        reservation_models.BookedDay.objects.get(
            day=date, reservation__room=room
        )  # __ is for the foreignkey
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False

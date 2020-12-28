from os import error
from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(
    takes_context=True
)  # If takes context is true, function's factor should be context, not request
def on_favs(context, room):
    user = context.request.user
    if user:
        the_list = list_models.List.objects.get_or_create(
            user=user, name="My Favourite Houses"
        )
        if the_list:
            return room in the_list.rooms.all()
        else:
            return "is not boolean"
    return "is not boolean"

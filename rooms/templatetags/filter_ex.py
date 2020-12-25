from django import template

register = template.Library()  # Neccessary


@register.filter(
    name="filter_ex"
)  # If we don't have filter_ex, filter name would be the functon name
def make_capital(value):
    return

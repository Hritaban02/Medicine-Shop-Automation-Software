from django import template

register = template.Library()

@register.filter
def dict(value, arg):
    return value[arg]
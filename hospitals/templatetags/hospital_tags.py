from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string by a delimiter. Usage: {{ value|split:',' }}"""
    return value.split(delimiter)

from django import template
register = template.Library()

@register.filter
def to(value, end):
    """Generates a range usable in for loops"""
    return range(value, end)
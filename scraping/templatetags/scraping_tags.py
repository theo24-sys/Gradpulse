from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def sector_badge(sector):
    """Returns the CSS class or style for a sector badge."""
    colors = {
        'government': 'background-color: #000080; color: white;',
        'ngo': 'background-color: #28a745; color: white;',
        'private': 'background-color: #6c757d; color: white;',
        'public': 'background-color: #20c997; color: white;',
        'international': 'background-color: #6f42c1; color: white;',
        'academic': 'background-color: #ffbf00; color: black;',
    }
    style = colors.get(sector.lower(), 'background-color: #eee; color: #333;')
    return mark_safe(f'style="{style}"')

@register.filter
def sector_name(sector):
    return sector.replace('_', ' ').title()

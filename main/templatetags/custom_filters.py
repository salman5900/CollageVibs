from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)  # Returns 0 if key not found

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)  # Returns 0 if key not found

@register.filter
def truncate_chars(value, max_length=150):
    if len(value) <= max_length:
        return value
    return value[:max_length - 3] + "..."

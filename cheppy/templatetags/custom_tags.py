from django import template

register = template.Library()

@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value

@register.simple_tag
def is_variable_updated(a, b):
    if a != b:
        return True
    return False

@register.simple_tag
def add_one(a):
    return a + 1
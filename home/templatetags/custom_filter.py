from django import template

register = template.Library()


@register.filter
def is_int(value):
    float_value = float(value)
    if float_value.is_integer():
        return True
    else:
        return False

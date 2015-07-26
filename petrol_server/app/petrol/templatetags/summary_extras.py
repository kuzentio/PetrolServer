from django import template

register = template.Library()

@register.filter(name='value_by_key')
def value_by_key(dict, key):
    return dict.get(key)

@register.filter(name='multipl')
def multipl(a, b):
    return a * b

@register.filter(name='minus')
def minus(a, b):
    return a - b

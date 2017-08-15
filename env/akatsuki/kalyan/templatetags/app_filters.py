from django import template
register = template.Library()
@register.filter(name='replace_space')
def replace_space(string):
    return string.replace(' ','_')
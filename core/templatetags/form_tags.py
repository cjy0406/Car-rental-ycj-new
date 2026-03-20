from django import template
register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={**field.field.widget.attrs, 'class': css})

@register.filter(name='hasattr')
def template_hasattr(obj, attr):
    return hasattr(obj, attr) 
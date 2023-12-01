from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.filter
def get_item_ava(dictionary, key):
    return dictionary.get(key)

@register.filter
def verify(dictionary, key):
    return str(key) in dictionary

@register.filter
def verify_item_dict(dictionary, key):
    if key in dictionary:
        return dictionary.get(key)
    else:
        return None
    
@register.filter
def get_all(manytomany):
    return manytomany.all()
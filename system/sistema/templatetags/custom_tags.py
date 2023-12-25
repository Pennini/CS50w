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

@register.simple_tag
def verify_events(dictionary, keyweek, keyday):
    count = 0
    points_group_area = {
        "areas": 2,
        "groups": 1
    }
    points_project_event = {
        "events": 11,
        "projects": 5,
    }
    for event in dictionary:
        if event in points_group_area and str(keyweek) in dictionary[event]:
            count += points_group_area.get(event, 0)
        if event in points_project_event and str(keyday) in dictionary[event]:
            count += points_project_event.get(event, 0)
            
    return count

@register.filter
def verify_into_list(position, list):
    return position in list
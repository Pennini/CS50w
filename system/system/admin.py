from django.contrib import admin

from .models import User, Group, Area, Position, Event, Project, Meeting, Availabilty

# Register your models here.
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Area)
admin.site.register(Position)
admin.site.register(Event)
admin.site.register(Project)
admin.site.register(Meeting)
admin.site.register(Availabilty)
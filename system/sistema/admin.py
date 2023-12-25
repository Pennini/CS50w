from django.contrib import admin

from .models import User, Group, Area, Position, Event, Project, Meeting, Availabilty

class ProjectAdmin(admin.ModelAdmin):
	filter_horizontal = ('members',)
	
class EventAdmin(admin.ModelAdmin):
    filter_horizontal = ('members_planned',)
    filter_horizontal = ('members_present',)

class MeetingAdmin(admin.ModelAdmin):
    filter_horizontal = ('members_present',)

# Register your models here.
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Area)
admin.site.register(Position)
admin.site.register(Event, EventAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Availabilty)
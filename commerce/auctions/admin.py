from django.contrib import admin

from .models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Auction)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)

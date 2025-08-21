from django.contrib import admin
from .models import Account, Driver, Rider, Trip, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Account)
admin.site.register(Driver)
admin.site.register(Rider)
admin.site.register(Trip)

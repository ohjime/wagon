from django.contrib import admin
from .models import Account, Driver, Rider, Trip

admin.site.register(Account)
admin.site.register(Driver)
admin.site.register(Rider)
admin.site.register(Trip)

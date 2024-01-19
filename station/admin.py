from django.contrib import admin

from station.models import Bus, Trip, Order, Ticket, Facility


admin.site.register(Bus)
admin.site.register(Trip)
admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(Facility)

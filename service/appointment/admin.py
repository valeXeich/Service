from django.contrib import admin

from .models import Location, Service, Schedule, Specialist, Appointment, TimeSlots, MyUser

admin.site.register(Location)
admin.site.register(Service)
admin.site.register(Schedule)
admin.site.register(Specialist)
admin.site.register(Appointment)
admin.site.register(TimeSlots)
admin.site.register(MyUser)


from django.contrib import admin

# Register your models here.
from Booking.models import voiture
from Booking.models import Reservation_voiture
admin.site.register(voiture)
admin.site.register(Reservation_voiture)
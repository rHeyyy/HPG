from django.contrib import admin
from .models import CustomUser, Owner, Pet, Service, Groomer, Appointment

admin.site.register(CustomUser)
admin.site.register(Pet)
admin.site.register(Service)
admin.site.register(Groomer)
admin.site.register(Appointment)

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    exclude = ('name',)
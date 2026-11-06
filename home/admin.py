from django.contrib import admin
from.models import UserProfile

# Register your models here.
from .models import booking, dept, doctors,contact
admin.site.register(dept)
admin.site.register(doctors)
admin.site.register(booking)
admin.site.register(contact)
admin.site.register(UserProfile)
from django.contrib import admin
from .models import UserBase

# Register your models here.
#Using default admin model with modified/extended db fields
admin.site.register(UserBase)

from django.contrib import admin

# Register your models here.
from .models import Plant, Irrigator, Specie

admin.site.register(Specie)
admin.site.register(Irrigator)
admin.site.register(Plant)

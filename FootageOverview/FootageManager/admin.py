from django.contrib import admin

from .models import Location, Footage, Camera

# Register your models here.
admin.site.register(Location)
admin.site.register(Camera)


@admin.register(Footage)
class FootageAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'footype', 'foocause')
    list_filter = ('footype', 'foocause')

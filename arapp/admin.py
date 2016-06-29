from django.contrib import admin
from .models import Appliance, Script, Action, Site

admin.site.register(Appliance)
admin.site.register(Script)
admin.site.register(Action)
admin.site.register(Site)

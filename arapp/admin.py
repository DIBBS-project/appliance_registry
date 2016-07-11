from django.contrib import admin
from .models import Appliance, ApplianceImpl, Script, Action, Site

admin.site.register(Appliance)
admin.site.register(ApplianceImpl)
admin.site.register(Script)
admin.site.register(Action)
admin.site.register(Site)

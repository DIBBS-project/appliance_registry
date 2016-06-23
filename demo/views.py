from django.shortcuts import render

import arapp.models as models


# Create your views here.
# Index that provides a description of the API
def appliances(request):
    appliancesp = models.Appliance.objects.all()
    return render(request, "appliances.html", {"appliances": appliancesp})

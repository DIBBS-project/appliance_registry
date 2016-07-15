from django.shortcuts import render

import arapp.models as models


def appliances(request):
    appliancesp = models.Appliance.objects.all()
    return render(request, "appliances.html", {"appliances": appliancesp})


def appliance_implementations(request):
    appliance_implementationsp = models.ApplianceImpl.objects.all()
    return render(request, "appliance_implementations.html", {"appliance_implementations": appliance_implementationsp})


def sites(request):
    sitesp = models.Site.objects.all()
    return render(request, "sites.html", {"sites": sitesp})


def actions(request):
    actionsp = models.Action.objects.all()
    return render(request, "actions.html", {"actions": actionsp})

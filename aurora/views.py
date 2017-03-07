# from django.shortcuts import render
from rest_framework import viewsets

from . import models
from . import serializers


class ApplianceViewSet(viewsets.ModelViewSet):
    queryset = models.Appliance.objects.all()
    serializer_class = serializers.ApplianceSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ImplementationViewSet(viewsets.ModelViewSet):
    queryset = models.Implementation.objects.all()
    serializer_class = serializers.ImplementationSerializer


class SiteViewSet(viewsets.ModelViewSet):
    queryset = models.Site.objects.all()
    serializer_class = serializers.SiteSerializer

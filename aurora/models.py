import uuid

from django.conf import settings
from django.db import models


class Appliance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)


class Implementation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appliance = models.ForeignKey('Appliance', related_name='implementations', on_delete=models.CASCADE)
    site = models.ForeignKey('Site', related_name='appliances', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=1000, blank=True)
    template = models.TextField(blank=True)
    template_parsed = models.TextField(editable=False) # always JSON


class Site(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100)  # Ex: openstack
    api_url = models.CharField(max_length=2048)

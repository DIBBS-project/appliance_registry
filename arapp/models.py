# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.db import models


class Appliance(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    logo_url = models.CharField(max_length=512, blank=True, default='')
    description = models.TextField(blank=True, default='')


class ApplianceImpl(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    logo_url = models.CharField(max_length=512, blank=True, default='')
    image_name = models.CharField(max_length=300)
    appliance = models.ForeignKey(Appliance, related_name='implementations', on_delete=models.CASCADE)
    site = models.ForeignKey("Site", related_name='appliances', on_delete=models.CASCADE)


class Site(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=100)  # Ex: openstack
    contact_url = models.CharField(max_length=2048)


class Action(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class Script(models.Model):
    code = models.TextField()

    # Relationships
    appliance = models.ForeignKey("ApplianceImpl", related_name='scripts', on_delete=models.CASCADE)
    action = models.ForeignKey("Action", related_name='scripts', on_delete=models.CASCADE)

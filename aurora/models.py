from django.conf import settings
from django.db import models


class Appliance(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    # logo_url = models.CharField(max_length=512, blank=True, default='')


# class Implementation(models.Model):
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     appliance = models.ForeignKey(Appliance, related_name='implementations', on_delete=models.CASCADE)
#     site = models.ForeignKey('Site', related_name='appliances', on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     script = models.TextField()

    # name = models.CharField(max_length=100, primary_key=True)
    # logo_url = models.CharField(max_length=512, blank=True, default='')
    # image_name = models.CharField(max_length=300)


class Site(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100)  # Ex: openstack
    api_url = models.CharField(max_length=2048)

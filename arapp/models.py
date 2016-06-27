from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Appliance(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class Action(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class Script(models.Model):
    code = models.TextField()

    # Relationships
    appliance = models.ForeignKey("Appliance", related_name='scripts', on_delete=models.CASCADE)
    action = models.ForeignKey("Action", related_name='scripts', on_delete=models.CASCADE)


# Add a token upon user creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(author=instance)

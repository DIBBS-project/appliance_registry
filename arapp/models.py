from django.db import models

# Create your models here.


class Software(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')


class Script(models.Model):
    code = models.TextField()
    link_to_template = models.TextField()

    # Relationships
    software = models.ForeignKey("Software", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)


class Event(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')

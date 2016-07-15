from django.conf.urls import url
from demo import views


urlpatterns = [
    url(r'^appliances/',  views.appliances),
    url(r'^appliance_implementations/',  views.appliance_implementations),
    url(r'^sites/',  views.sites),
    url(r'^actions/',  views.actions),
]

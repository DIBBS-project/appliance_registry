from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
import rest_framework.authtoken.views
from arapp import views
# from rest_framework_jwt.views import obtain_jwt_token

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'scripts', views.ScriptViewSet)
router.register(r'softwares', views.SoftwareViewSet)

import demo.views as demo_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webservice.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Users
    url(r'^register_new_user/?$', views.register_new_user),

    # # Softwares
    # url(r'^softwares/?$', views.software_list),
    # url(r'^softwares/(?P<pk>[0-9]+)/$', views.software_detail),
    #
    # # Scripts
    # url(r'^scripts/?$', views.script_list),
    # url(r'^scripts/(?P<pk>[0-9]+)/$', views.script_detail),
    #
    # # Events
    # url(r'^events/?$', views.event_list),
    # url(r'^events/(?P<pk>[0-9]+)/$', views.event_detail),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Token
    # url(r'^api-token-auth/', obtain_jwt_token),

    # Demo
    url(r'^demo/', include('demo.urls')),

)

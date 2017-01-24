# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from arapp import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'actions', views.ActionViewSet)
router.register(r'scripts', views.ScriptViewSet)
router.register(r'appliances', views.ApplianceViewSet)
router.register(r'appliances_impl', views.ApplianceImplViewSet)
router.register(r'sites', views.SiteViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', views.debug_view),
    url(r'^', include(router.urls)),
    url(r'^scripts/(?P<appliance_impl_name>.+)/(?P<action>.+)/$', views.ScriptForApplianceAndAction.as_view()),

    # Demo
    url(r'^demo/', include('demo.urls')),
]

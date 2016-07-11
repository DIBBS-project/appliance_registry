from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from arapp import views
import rest_framework.authtoken.views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'actions', views.ActionViewSet)
router.register(r'scripts', views.ScriptViewSet)
router.register(r'appliances', views.ApplianceViewSet)
router.register(r'appliances_impl', views.ApplianceImplViewSet)
router.register(r'sites', views.SiteViewSet)

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(router.urls)),
    url(r'^scripts/(?P<appliance_impl_name>.+)/(?P<action>.+)/$', views.ScriptForApplianceAndAction.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Demo
    url(r'^demo/', include('demo.urls')),

)

# Allows to get a token by sending credentials
urlpatterns += [
    url(r'^api-token-auth/', rest_framework.authtoken.views.obtain_auth_token)
]

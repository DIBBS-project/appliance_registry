from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'actions', views.ActionViewSet)
# router.register(r'scripts', views.ScriptViewSet)
# router.register(r'appliances_impl', views.ApplianceImplViewSet)
router.register(r'appliances', views.ApplianceViewSet)
router.register(r'sites', views.SiteViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^test/', views.debug_view),
    url(r'^', include(router.urls)),
]

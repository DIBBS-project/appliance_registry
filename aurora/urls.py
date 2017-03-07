from django.conf.urls import include, url
# from django.contrib import admin
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'appliances', views.ApplianceViewSet)
router.register(r'implementations', views.ImplementationViewSet)
router.register(r'sites', views.SiteViewSet)

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^test/', views.debug_view),
    url(r'^', include(router.urls)),
]

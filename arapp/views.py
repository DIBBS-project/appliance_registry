# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

import json

from django.http import Http404, HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from arapp.models import Appliance, ApplianceImpl, Script, Action, Site
from arapp.serializers import ApplianceSerializer, ApplianceImplSerializer, ScriptSerializer, ActionSerializer, SiteSerializer


def debug_view(request):
    return HttpResponse(json.dumps({
        'user': str(request.user),
        'type(user)': str(type(request.user)),
        'is_authenticated': bool(request.user.is_authenticated()),
        'is_anonymous': bool(request.user.is_anonymous()),
        'is_active': bool(request.user.is_active),
        'dibbs_interservice': str(request.dibbs_interservice),
    }))


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'appliances': reverse('appliance-list', request=request, format=format),
        'scripts': reverse('script-list', request=request, format=format),
        'actions': reverse('action-list', request=request, format=format),
        'sites': reverse('site-list', request=request, format=format)
    })


class ApplianceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Appliance.objects.all()
    serializer_class = ApplianceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        data2[u'implementations'] = {}
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ApplianceImplViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ApplianceImpl.objects.all()
    serializer_class = ApplianceImplSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        data2[u'scripts'] = {}
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SiteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        data2[u'appliances'] = {}
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ScriptViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ScriptForApplianceAndAction(APIView):

    def get_appliance_impl(self, name):
        try:
            return ApplianceImpl.objects.get(name=name)
        except ApplianceImpl.DoesNotExist:
            raise Http404

    def get_script(self, ids):
        try:
            return Script.objects.get(id=ids)
        except Script.DoesNotExist:
            raise Http404

    def get(self, request, appliance_impl_name, action, format=None):
        app_impl = self.get_appliance_impl(appliance_impl_name)
        for script in app_impl.scripts.all():
            if script.action.name == action:
                serializer = ScriptSerializer(script)
                return Response(serializer.data)

        app_impl = self.get_appliance_impl(u'common')
        for script in app_impl.scripts.all():
            if script.action.name == action:
                serializer = ScriptSerializer(script)
                return Response(serializer.data)

        raise Http404


class ActionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        data2[u'scripts'] = {}
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

from arapp.models import Appliance, Script, Action, Site
from arapp.serializers import ApplianceSerializer, ScriptSerializer, ActionSerializer, UserSerializer, SiteSerializer

# from django.views.decorators.csrf import csrf_exempt

from django.http import Http404

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'appliances': reverse('appliance-list', request=request, format=format),
        'scripts': reverse('script-list', request=request, format=format),
        'actions': reverse('action-list', request=request, format=format),
        'sites': reverse('site-list', request=request, format=format)
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
    def get_appliance(self, name):
        try:
            return Appliance.objects.get(name=name)
        except Appliance.DoesNotExist:
            raise Http404

    def get_script(self, ids):
        try:
            return Script.objects.get(id=ids)
        except Script.DoesNotExist:
            raise Http404

    def get(self, request, appliance, action, format=None):
        app = self.get_appliance(appliance)
        for script in app.scripts.all():
            if script.action.name == action:
                serializer = ScriptSerializer(script)
                return Response(serializer.data)
        app = self.get_appliance(u'common')
        for script in app.scripts.all():
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

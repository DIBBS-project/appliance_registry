from arapp.models import Appliance, Script, Action
from arapp.serializers import ApplianceSerializer, ScriptSerializer, ActionSerializer, UserSerializer

# from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'appliances': reverse('appliance-list', request=request, format=format),
        'scripts': reverse('script-list', request=request, format=format),
        'actions': reverse('action-list', request=request, format=format)
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


class ScriptViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


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

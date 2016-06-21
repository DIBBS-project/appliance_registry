from arapp.models import Software, Script, Event
from arapp.serializers import SoftwareSerializer, ScriptSerializer, EventSerializer

from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http import HttpResponse

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


##############################
# User management
##############################


@api_view(['POST'])
@csrf_exempt
def register_new_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    logger.debug("will create user (%s, %s)" % (username, password))

    from django.contrib.auth.models import User
    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
    except:
        return Response({"status": "failed"})

    return Response({"status": "ok"})


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'processdefs': reverse('processdef-list', request=request, format=format)
    })


class SoftwareViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
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


class EventViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
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


# # Methods related to Software
# @api_view(['GET', 'POST'])
# @csrf_exempt
# def software_list(request):
#     """
#     List all softwares, or create a new software.
#     """
#     if request.method == 'GET':
#         softwares = Software.objects.all()
#         serializer = SoftwareSerializer(softwares, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SoftwareSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# @csrf_exempt
# def software_detail(request, pk):
#     """
#     Retrieve, update or delete a software.
#     """
#     try:
#         software = Software.objects.get(pk=pk)
#     except Software.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = SoftwareSerializer(software)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = SoftwareSerializer(software, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         software.delete()
#         return HttpResponse(status=204)
#
#
# # Methods related to Script
# @api_view(['GET', 'POST'])
# @csrf_exempt
# def script_list(request):
#     """
#     List all code snippets, or create a new script.
#     """
#     if request.method == 'GET':
#         scripts = Script.objects.all()
#         serializer = ScriptSerializer(scripts, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ScriptSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# @csrf_exempt
# def script_detail(request, pk):
#     """
#     Retrieve, update or delete a script.
#     """
#     try:
#         script = Script.objects.get(pk=pk)
#     except Script.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = ScriptSerializer(script)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = ScriptSerializer(script, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         script.delete()
#         return HttpResponse(status=204)
#
#
# # Methods related to Script
# @api_view(['GET', 'POST'])
# @csrf_exempt
# def event_list(request):
#     """
#     List all events, or create a new event.
#     """
#     if request.method == 'GET':
#         events = Event.objects.all()
#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = EventSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# @csrf_exempt
# def event_detail(request, pk):
#     """
#     Retrieve, update or delete an event.
#     """
#     try:
#         event = Event.objects.get(pk=pk)
#     except Event.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = EventSerializer(event)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = EventSerializer(event, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         event.delete()
#         return HttpResponse(status=204)

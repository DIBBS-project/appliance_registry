from rest_framework import serializers
from models import Appliance, Script, Action
from django.contrib.auth.models import User


class ApplianceSerializer(serializers.ModelSerializer):
    scripts = serializers.PrimaryKeyRelatedField(many=True, queryset=Script.objects.all())

    class Meta:
        model = Appliance
        fields = ('name', 'scripts')


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ('id', 'code', 'software', 'event')


class ActionSerializer(serializers.ModelSerializer):
    scripts = serializers.PrimaryKeyRelatedField(many=True, queryset=Script.objects.all())

    class Meta:
        model = Action
        fields = ('name', 'scripts')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

from rest_framework import serializers
from models import Appliance, ApplianceImpl, Script, Action, Site
from django.contrib.auth.models import User


class ApplianceSerializer(serializers.ModelSerializer):
    implementations = serializers.PrimaryKeyRelatedField(many=True, queryset=ApplianceImpl.objects.all())

    class Meta:
        model = Appliance
        fields = ('name', 'implementations')


class ApplianceImplSerializer(serializers.ModelSerializer):
    scripts = serializers.PrimaryKeyRelatedField(many=True, queryset=Script.objects.all())

    class Meta:
        model = ApplianceImpl
        fields = ('name', 'image_name', 'site', 'scripts', 'appliance')


class SiteSerializer(serializers.ModelSerializer):
    appliances = serializers.PrimaryKeyRelatedField(many=True, queryset=ApplianceImpl.objects.all())

    class Meta:
        model = Site
        fields = ('name', 'contact_url', 'appliances')


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ('id', 'code', 'appliance', 'action')


class ActionSerializer(serializers.ModelSerializer):
    scripts = serializers.PrimaryKeyRelatedField(many=True, queryset=Script.objects.all())

    class Meta:
        model = Action
        fields = ('name', 'scripts')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

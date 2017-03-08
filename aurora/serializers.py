from rest_framework import serializers

from . import models


class ApplianceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Appliance
        fields = '__all__'

    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    # implementations = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='implementations-detail',
    # )


class ImplementationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Implementation
        fields = '__all__'

    site = serializers.HyperlinkedRelatedField(
        view_name='site-detail',
        queryset=models.Site.objects.all(),
    )
    appliance = serializers.HyperlinkedRelatedField(
        view_name='appliance-detail',
        queryset=models.Appliance.objects.all(),
    )
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Site
        fields = '__all__'

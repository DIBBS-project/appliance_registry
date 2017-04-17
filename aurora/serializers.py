import json

from rest_framework import serializers
import yaml

from . import models


def parse_template(yaml_script):
    """
    Convert YAML script into JSON. Fails if there's an error.
    """
    try:
        template = yaml.safe_load(yaml_script)
    except yaml.scanner.ScannerError as e:
        raise ValueError(e)

    # the heat client doesn't like dates, which PyYAML helpfully deserialized for us...
    HTV = 'heat_template_version'
    if HTV in template:
        template[HTV] = template[HTV].strftime('%Y-%m-%d')

    try:
        parsed = json.dumps(template)
    except TypeError as e:
        raise ValueError(e)

    return parsed


class ApplianceSerializer(serializers.ModelSerializer):
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


class ImplementationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Implementation
        fields = '__all__'

    site = serializers.PrimaryKeyRelatedField(
        queryset=models.Site.objects.all(),
    )
    appliance = serializers.PrimaryKeyRelatedField(
        queryset=models.Appliance.objects.all(),
    )
    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    def validate_script(self, value):
        try:
            self._script_parsed = parse_template(value)
        except ValueError:
            raise serializers.ValidationError('could not parse script as YAML')
        return value

    def validate(self, data):
        # named field validators run first, and the script one did the
        # checking, but we need to plug it in here.
        data['script_parsed'] = self._script_parsed
        return data


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Site
        fields = '__all__'

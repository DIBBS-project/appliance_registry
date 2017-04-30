import json

import jinja2
from rest_framework import serializers
import yaml

from . import models


JINJA_ENV = jinja2.Environment(loader=jinja2.PackageLoader('aurora', 'templates'))


def template_deserialize_yaml(yaml_template):
    """
    Deserialize YAML template. Fails if there's an error.
    """
    try:
        template = yaml.safe_load(yaml_template)
    except yaml.scanner.ScannerError as e:
        raise serializers.ValidationError('could not parse script as YAML')

    # the heat client doesn't like dates, which PyYAML helpfully deserialized for us...
    HTV = 'heat_template_version'
    if HTV in template:
        template[HTV] = template[HTV].strftime('%Y-%m-%d')

    return template


def template_serialize_json(template):
    """
    Reserialize template into JSON. Fails if there's an error, probably from
    unseriazable field like a date that snuck through.
    """
    try:
        parsed = json.dumps(template)
    except TypeError as e:
        raise serializers.ValidationError('could not serialize script to JSON')

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

    def validate_template(self, raw_template):
        template = template_deserialize_yaml(raw_template)

        # TODO distinguish between "LL apps" and generic complex appliances that
        # don't need to have specific outputs. LL apps must output/take some
        # other values.
        try:
            template['outputs']['master_ip']
        except KeyError:
            raise serializers.ValidationError('no "master_ip" output in template')

        if raw_template:
            self._template_parsed = template_serialize_json(template)
        return raw_template

    def validate_image(self, image_name):
        template_template = JINJA_ENV.get_template('simple_app.jinja2')
        generated_template = template_template.render(image=image_name)

        template = template_deserialize_yaml(generated_template)
        # checks? we control the template though...but a "special" image name
        # could do some strange things.
        if image_name:
            self._template_parsed = template_serialize_json(template)
        return image_name

    def validate(self, data):
        # named field validators run first, and the script one did the
        # checking, but we need to plug it in here.
        image = data.get('image')
        template = data.get('template')
        if image and template:
            raise serializers.ValidationError('provide one of "image" and "template", not both')
        if not (image or template):
            raise serializers.ValidationError('provide one of "image" and "template"')

        data['template_parsed'] = self._template_parsed
        return data


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Site
        fields = '__all__'

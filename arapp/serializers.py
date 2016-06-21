from rest_framework import serializers
from models import Software, Script, Event


class SoftwareSerializer(serializers.ModelSerializer):
    scripts = serializers.PrimaryKeyRelatedField(many=True, queryset=Script.objects.all())

    class Meta:
        model = Software
        fields = ('id', 'name', 'scripts')


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ('id', 'code', 'software', 'event')


class EventSerializer(serializers.ModelSerializer):
    scripts = serializers.PrimaryKeyRelatedField(many=True, queryset=Script.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'name', 'scripts')


# class SoftwareSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=100, allow_blank=True, default='')
#
#     script_ids = serializers.SerializerMethodField('software_scripts')
#
#     def software_scripts(self, software):
#         return map(lambda x: x.id, Script.objects.filter(software_id=software.id))
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Software` instance, given the validated data.
#         """
#         return Software.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Software` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#
#         if instance.name != "":
#             instance.save()
#         return instance
#
#
# class ScriptSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     code = serializers.CharField()
#     link_to_template = serializers.CharField()
#
#     # Relationships
#     software_id = serializers.IntegerField(read_only=True)
#     event_id = serializers.IntegerField(read_only=True)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Cluster` instance, given the validated data.
#         """
#         return Script.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Cluster` instance, given the validated data.
#         """
#         instance.code = validated_data.get('code', instance.name)
#         instance.link_to_template = validated_data.get('link_to_template', instance.site)
#
#         software_id = validated_data.get('software_id', instance.software.id)
#         if software_id is not None:
#             software = Software.objects.filter(id=software_id).first()
#             instance.software = software
#
#         event_id = validated_data.get('event_id', instance.event.id)
#         if event_id is not None:
#             event = Event.objects.filter(id=event_id).first()
#             instance.event = event
#
#         if instance.code != "" and instance.link_to_template != "":
#             instance.save()
#         return instance
#
#
# class EventSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=100, allow_blank=True, default='')
#
#     scripts_ids = serializers.SerializerMethodField('event_scripts')
#
#     def event_scripts(self, event):
#         return map(lambda x: x.id, Script.objects.filter(event_id=event.id))
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Event` instance, given the validated data.
#         """
#         return Event.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Event` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#
#         if instance.name != "":
#             instance.save()
#         return instance

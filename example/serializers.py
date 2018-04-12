
from rest_framework import serializers
from .models import Alarm, AlarmEvent

class AlarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alarm
        fields = ('id', 'name', 'slug', 'duration', 'description')


class AlarmEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlarmEvent
        fields = ('id', 'alarm', 'alarm_type', 'created', 'finished', 'content_type', 'description')
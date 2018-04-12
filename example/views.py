from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db.models import Q
from django_filters import rest_framework as filters
from django.http import Http404
from .models import Alarm, AlarmEvent
from .serializers import AlarmEventSerializer, AlarmSerializer

# Create your views here.
class AlarmList(APIView):

    ''' List all Alarm, or create a new Alarm'''

    def get(self, request, format=None):
        ''' Get all alarms '''
        alarms = Alarm.objects.all()
        serializer = AlarmSerializer(alarms, many=True)
        return Response(serializer.data)

    def post(self, request):
        ''' Post an alarm via POST Method'''
        serializer = AlarmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlarmDetail(APIView):

    ''' GET, PUT AND DELETE METHODS FOR Monitor '''

    def get_object(self, pk):
        try:
            return Alarm.objects.get(pk=pk)
        except Alarm.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ''' Get a Alarm by PK '''
        try:
            alarm = Alarm.objects.get(pk=pk)
            serializer = AlarmSerializer(alarm)
            return Response(serializer.data)
        except Alarm.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        ''' Put information in a existing alarm by pk'''
        try:
            alarm = Alarm.objects.get(pk=pk)
            serializer = AlarmSerializer(alarm, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Alarm.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        ''' Delete an existing alarm by pk'''
        alarm = self.get_object(pk=pk)
        alarm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# fin vistas Alarm

# vistas AlarmEvent


class AlarmEventList(generics.ListAPIView):

    ''' List AlarmEvents by filters, or create a new AlarmEvent '''


    def get_queryset(self):
        ''' Getting events which the user is subscribed '''
        return AlarmEvent.objects.all()

    def post(self, request, format=None):
        ''' Create new event '''
        serializer = AlarmEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlarmEventDetail(APIView):

    ''' GET, PUT AND DELETE METHODS FOR AlarmEvent '''

    def get_object(self, pk):
        try:
            return AlarmEvent.objects.get(pk=pk)

        except AlarmEvent.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        ''' Get event information by pk, if the user is subscribed to this '''
        try:
            event = AlarmEvent.objects.get(pk=pk)
            serializer = AlarmEventSerializer(event)
            my_events = AlarmEventList.get_queryset(self)
            if event in my_events:
                return Response(serializer.data)
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Not Authorized User"})
        except AlarmEvent.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # if notification does not exist

    def delete(self, request, pk, format=None):
        ''' Delete event object '''
        event = self.get_object(pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.conf.urls import url
from .views import AlarmEventList, AlarmEventDetail, AlarmList, AlarmDetail
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView

urlpatterns = [
    ### API endpoints ###
    url(r'api/alarms/$', AlarmList.as_view(), name='alarms_list'),
    url(r'api/alarms/(?P<pk>[0-9]+)/$', AlarmDetail.as_view(), name='alarms_detail'),
    url(r'api/alarms/events/$', AlarmEventList.as_view(), name='events_list'),
    url(r'api/alarms/events/(?P<pk>[0-9]+)', AlarmEventDetail.as_view(), name='events_detail')
    ### END API endpoints ###

]

urlpatterns = format_suffix_patterns(urlpatterns)
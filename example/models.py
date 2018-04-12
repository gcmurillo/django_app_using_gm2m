from django.db import models
from gm2m import GM2MField

# Create your models here.

class Alarm(models.Model):

    name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(blank=True, max_length=80)
    # Acccion - codigo a ejecutar con las variables asociadas
    duration = models.IntegerField(default=0)  # duracion en horas
    description = models.CharField(max_length=255, default='default')


class AlarmEvent(models.Model):
    # Alarm types

    USER = 'US'
    DEVICE = 'DV'
    NO_DEVICE = 'ND'

    ALARM_CHOICES = (
        (USER, 'User'),
        (DEVICE, 'Device'),
        (NO_DEVICE, 'No-Device')
    )

    alarm = models.ForeignKey(Alarm, on_delete=models.CASCADE, null=True)
    alarm_type = models.CharField(max_length=2, choices=ALARM_CHOICES, default=USER)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True)
    content_type = GM2MField()
    description = models.CharField(max_length=255, default='description', null=True)

    def get_contents_type(self):
        return "\n".join(obj.__str__() + '|' for obj in self.content_type.all())

    def __str__(self):
        return self.alarm_type + '-' + str(self.pk)
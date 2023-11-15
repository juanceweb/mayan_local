from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


##################################################################################
# SOLICITUD GENERAL
################################################################################## 
class Solicitud(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(f'Solicitud({self.id})')        

    class Meta:
        verbose_name = _('Solicitud')
        verbose_name_plural = _('Solicitudes')
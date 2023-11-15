from django.db import models
from django.utils.translation import ugettext_lazy as _
from .solicitud import Solicitud

##################################################################################
# SOLICITUD CAMPOS
################################################################################## 
class Solicitud_Campo(models.Model):

    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, null=True)

    nombre_campo = models.CharField(max_length=255, help_text=_('nombre de campo.'), verbose_name=_('nombre de campo'))

    valor_campo = models.CharField(max_length=255, help_text=_('valor de campo.'), verbose_name=_('valor de campo'))

    def __str__(self):
        return str(f'Solicitud Campo({self.nombre_campo} = {self.valor_campo})')        

    class Meta:
        verbose_name = _('Solicitud Campo')
        verbose_name_plural = _('Solicitud Campos')
        

##################################################################################
# SOLICITUD CAMPO TIPO
################################################################################## 
class Solicitud_Campo_Tipo(models.Model):

    nombre_campo = models.CharField(max_length=255, help_text=_('nombre de campo.'), verbose_name=_('nombre de campo'))

    tipo_campo = models.CharField(max_length=255, help_text=_('tipo de campo.'), verbose_name=_('tipo de campo'))

    def __str__(self):
        return str(f'Solicitud Tipo Campo({self.nombre_campo} = {self.tipo_campo})')        

    class Meta:
        verbose_name = _('Solicitud Campo Tipo')
        verbose_name_plural = _('Solicitud Campos Tipo')



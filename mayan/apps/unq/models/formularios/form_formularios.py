from django.db import models
from django.utils.translation import ugettext_lazy as _

###################################################################################
# FORMULARIOS 
###################################################################################
class Form_Formulario (models.Model):

    solicitud = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'nombre de la solicitud.'
        ),
        verbose_name=_('solicitud')
        )
        
    def __str__(self):
        return str(f'Form({self.solicitud})')
        
    class Meta:
        verbose_name = _('Formulario')
        verbose_name_plural = _('Formularios')


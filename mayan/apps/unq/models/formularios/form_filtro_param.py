from django.db import models
from django.utils.translation import ugettext_lazy as _

###################################################################################
# FILTRO PARAM
###################################################################################
class Form_Filtro_Param (models.Model):
    
    identificador =  models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'identificador de accion.'
        ),
        verbose_name=_('identificador')
        )
    
    def __str__(self):
        return str(f'Filtro Param ({self.identificador})')

    class Meta:
        verbose_name = _('Formulario Filtro Param')
        verbose_name_plural = _('Formulario Filtro Params')



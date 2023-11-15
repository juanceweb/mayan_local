from django.db import models
from django.utils.translation import ugettext_lazy as _

###################################################################################
# ACCION
###################################################################################
class Form_Accion (models.Model):
    
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
        return str(f'Accion ({self.identificador})')

    class Meta:
        verbose_name = _('Formulario Accion')
        verbose_name_plural = _('Formulario Acciones')

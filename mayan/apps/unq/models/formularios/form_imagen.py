from django.db import models
from django.utils.translation import ugettext_lazy as _

###################################################################################
# IMAGEN
###################################################################################
class Form_Imagen (models.Model):

    identificador = models.CharField(
        max_length=255,
        help_text=_(
            'identificador.'
        ),
        verbose_name=_('identificador')
        )
    
    ruta = models.CharField(
        max_length=255,
        help_text=_(
            'ruta a la imagen.'
        ),
        verbose_name=_('ruta')
        )
    
    label = models.CharField(
        max_length=10,
        default='imagen',
        editable=False,
        help_text=_(
            'imagen.'
        ),
        verbose_name=_('imagen')
        )
    
    def __str__(self):
        return str(f'Imagen({self.identificador})')
        
    class Meta:
        verbose_name = _('Formulario Imagen')
        verbose_name_plural = _('Formulario Imagenes')
from django.db import models
from django.utils.translation import ugettext_lazy as _

###################################################################################
# TEXTO
###################################################################################
class Form_Texto (models.Model):

    texto = models.TextField(
        max_length=255,
        help_text=_(
            'texto.'
        ),
        verbose_name=_('texto')
        )
    
    etiqueta = models.CharField(
        max_length=255,
        help_text=_(
            'etiqueta html.'
        ),
        verbose_name=_('etiqueta html ')
        )

    label = models.CharField(
        max_length=10,
        default='texto',
        editable=False,
        help_text=_(
            'texto.'
        ),
        verbose_name=_('texto')
        )

          
    def __str__(self):
        return str(f'Texto({self.texto})')
        
    class Meta:
        verbose_name = _('Formulario Texto')
        verbose_name_plural = _('Formulario Textos')
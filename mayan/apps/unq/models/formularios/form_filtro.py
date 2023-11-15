from django.db import models
from django.utils.translation import ugettext_lazy as _

###################################################################################
#  FILTRO
###################################################################################
class Form_Filtro (models.Model):

    tipo = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'tipo.'
        ),
        verbose_name=_('tipo')
        )
    
    valor = models.IntegerField(
        null=True,
        blank=True,
        help_text=_(
            'valor.'
        ),
        verbose_name=_('valor')
        )
    
    def get_valor(self):
        return self.valor
    
    def __str__(self):
        return str(f'Filtro({self.tipo} : {self.valor})')

    class Meta:
        ordering = ('id',)
        verbose_name = _('Formulario Filtro')
        verbose_name_plural = _('Formulario Filtros')

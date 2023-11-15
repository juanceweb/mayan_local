from django.db import models
from django.utils.translation import ugettext_lazy as _

###################################################################################
# ELEMENTO
###################################################################################
class Form_Elemento (models.Model):

    tipo = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'tipo.'
        ),
        verbose_name=_('tipo')
        )
    
    readonly = models.BooleanField(
        null=True,
        blank=True,
        help_text=_(
            'readonly.'
        ),
        verbose_name=_('readonly')
        )
    
    def get_dict(self):

        element_dict = {}

        if self.tipo != None:
            element_dict.update({"tipo" : self.tipo})
        if self.readonly != None:
            element_dict.update({"readonly": self.readonly})

        return element_dict
    
    def __str__(self):
        return str(f'Elemento({self.tipo})')

    class Meta:
        ordering = ('id',)
        verbose_name = _('Formulario Elemento')
        verbose_name_plural = _('Formulario Elementos')
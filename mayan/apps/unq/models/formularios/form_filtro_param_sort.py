from django.db import models
from django.utils.translation import ugettext_lazy as _
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey
from .form_filtro_param import Form_Filtro_Param


###################################################################################
# FILTRO PARAMS SORTEABLE
###################################################################################
class Form_Filtro_Params_Sorteable (SortableMixin):

    form = SortableForeignKey(Form_Filtro_Param,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_('multi option'),
        verbose_name=_('multi option')
        )
    
    clave = models.CharField(
        max_length=255,
        blank=True,
        help_text=_(
            'clave.'
        ),
        verbose_name=_('clave')
        )
    
    valor = models.CharField(
        max_length=255,
        help_text=_(
            'valor.'
        ),
        verbose_name=_('valor')
        )
    
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
 
    def __str__(self):
        return str(f'Filtro Param Sorteable({self.form})')        

    class Meta:
        ordering = ['order']
        verbose_name = _('Filtro Params Sorteable')
        verbose_name_plural = _('Filtro Params Sorteable')

from django.db import models
from django.utils.translation import ugettext_lazy as _
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey
from .form_accion import Form_Accion


###################################################################################
# ACTION SORTEABLE
###################################################################################
class Form_Accion_Sorteable (SortableMixin):

    ELEM_CHOICES = ( 
    ('archivo','ARCHIVO'),
    ('texto','TEXTO'),
    ('imagen', 'IMAGEN'),
    ('key', 'CAMPO(KEY)'),
    ('label', 'CAMPO(LABEL)'),
    ('elemento_html', 'CAMPO(ELEMENTO_HTML)'),
    ('filtro', 'CAMPO(FILTRO)'),
    ('obligatorio', 'CAMPO(OBLIGATORIO)'),
    ('largo', 'CAMPO(LARGO)'),
    ('multiOptions', 'CAMPO(MULTI OPTION)'),
    ('readonly', 'CAMPO(READONLY)'),
    ('rows', 'CAMPO(ROWS)'),
    ('default', 'CAMPO(DEFAULT)'),
    ('placeholder', 'CAMPO(PLACEHOLDER)'),
    ('clase_css', 'CAMPO(CLASE_CSS)'),
    ('validar_select', 'CAMPO(VALIDAR_SELECT)'),
    ('checked_value', 'CAMPO(CHECKED_VALUE)'),
    ('unchecked_value', 'CAMPO(UNCHECKED_VALUE)'),
    )


    form = SortableForeignKey(Form_Accion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_('accion'),
        verbose_name=_('accion')
        )
    
    elemento = models.CharField( max_length=255, choices=ELEM_CHOICES )
    
    accion = models.CharField(
        max_length=255,
        help_text=_(
            'accion.'
        ),
        verbose_name=_('accion')
        )
    
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
 
    def __str__(self):
        return str(f'Accion Sorteable({self.accion})')        

    class Meta:
        ordering = ['order']
        verbose_name = _('Accion Sorteable')
        verbose_name_plural = _('Accion Sorteable')
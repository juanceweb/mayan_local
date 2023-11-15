from django.db import models
from django.utils.translation import ugettext_lazy as _
from .form_elemento import Form_Elemento
from .form_filtro import Form_Filtro
from .form_filtro_param import Form_Filtro_Param
from .form_multi import Form_Multi_Option


###################################################################################
# CAMPOS
###################################################################################
class Form_Campo (models.Model):

    key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'key elemento.'
        ),
        verbose_name=_('key')
        )
    
    label = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'label.'
        ),
        verbose_name=_('label')
        )

    elemento_html = models.ForeignKey(Form_Elemento,
        related_name='form_tipo',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text=_('elemento.'),
        verbose_name=_('elemento')
        )
    
    filtro = models.ForeignKey(Form_Filtro,
        related_name='form_filtro',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text=_('filtro.'),
        verbose_name=_('filtro')
        )
    
    filtro_params = models.ForeignKey(Form_Filtro_Param,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text=_('filtro params.'),
        verbose_name=_('filtro params')
        )
    
    obligatorio = models.BooleanField(
        null=True,
        blank=True,
        help_text=_(
            'obligatorio.'
        ),
        verbose_name=_('obligatorio')
        )
    
    largo = models.IntegerField(
        null=True,
        blank=True,
        help_text=_(
            'largo.'
        ),
        verbose_name=_('largo')
        )
    
    multiOptions = models.ForeignKey(Form_Multi_Option,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text=_('multi options.'),
        verbose_name=_('multi options'))
    
    readonly = models.BooleanField(
        null=True,
        blank=True,
        help_text=_(
            'readonly.'
        ),
        verbose_name=_('readonly')
        )
    
    rows = models.IntegerField(
        null=True,
        blank=True,
        help_text=_(
            'rows.'
        ),
        verbose_name=_('rows')
        )
    
    default = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'default.'
        ),
        verbose_name=_('default')
        )
     
    placeholder = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'placeholder.'
        ),
        verbose_name=_('placeholder')
        )
    
    clase_css = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'clase css.'
        ),
        verbose_name=_('clase css')
        )
    
    validar_select = models.BooleanField(
        null=True,
        blank=True,
        help_text=_(
            'validar select.'
        ),
        verbose_name=_('validar select')
        )

    checked_value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'checked value.'
        ),
        verbose_name=_('checked value')
        )
    
    unchecked_value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_(
            'unchecked value.'
        ),
        verbose_name=_('unchecked value')
        )
    
       
    def __str__(self):
        return str(f'Campo({self.key})')        

    class Meta:
        ordering = ['id']
        verbose_name = _('Formulario Campo')
        verbose_name_plural = _('Formulario Campos')
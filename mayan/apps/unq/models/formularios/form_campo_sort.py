from django.db import models
from django.utils.translation import ugettext_lazy as _
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey
from .form_formularios import Form_Formulario
from .form_imagen import Form_Imagen
from .form_accion import Form_Accion
from .form_texto import Form_Texto
from .form_campo import Form_Campo

###################################################################################
# CAMPOS SORTEABLE
###################################################################################
class Form_Campo_Sorteable (SortableMixin):

    LINEA_CHOICES = ( 
    ('primero','PRIMERO'),
    ('medio','MEDIO'),
    ('ultimo', 'ULTIMO'),
    )

    form = SortableForeignKey(Form_Formulario,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_('formulario'),
        verbose_name=_('formulario')
        )
    
    field = models.ForeignKey(Form_Campo,on_delete=models.CASCADE, null=True, blank=True, help_text=_('campo.'),verbose_name=_('campo'))
    text = models.ForeignKey(Form_Texto,on_delete=models.CASCADE, null=True, blank=True, help_text=_('campo texto.'),verbose_name=_('texto'))
    file = models.BooleanField(help_text=_('campo archivo.'),verbose_name=_('archivo'))
    image = models.ForeignKey(Form_Imagen,on_delete=models.CASCADE, null=True, blank=True, help_text=_('imagen.'),verbose_name=_('imagen'))
    action = models.ForeignKey(Form_Accion, on_delete=models.CASCADE, null=True, blank=True, help_text=_('accion.'),verbose_name=_('accion'))
    form_error = models.BooleanField(help_text=_('errores del form.'),verbose_name=_('form errors'))
    form_message = models.BooleanField(help_text=_('mensajes del form.'),verbose_name=_('form mensajes'))
    form_same_line = models.CharField( max_length=255, null=True, blank=True, choices=LINEA_CHOICES )

    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def define_type(self):
        if self.field != None and (self.text == None and self.image == None):
            type = 'Campo'
        elif self.text != None and (self.field == None and self.image == None):
            type = 'Texto'
        elif self.image != None and (self.field == None and self.text == None):
            type = 'Imagen'
        elif self.field == None and self.text == None and self.file == False:
            type = 'None'
        else:
            type = 'Error'
        
        return type
        

    def get_type(self):
        type = self.define_type()
        return type

    def get_action(self):
        if self.action != None:
            return True
 
    def __str__(self):
        type = self.define_type()
        return type

    class Meta:
        ordering = ['order']
        verbose_name = _('Campo Sorteable')
        verbose_name_plural = _('Campos Sorteable')


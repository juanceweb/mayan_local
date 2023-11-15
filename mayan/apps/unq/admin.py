from django.contrib import admin
from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline

from .models.permisos.permisos import PermisosUNQ

from .models.formularios.form_accion_sort import Form_Accion_Sorteable
from .models.formularios.form_accion import Form_Accion
from .models.formularios.form_campo_sort import Form_Campo_Sorteable
from .models.formularios.form_campo import Form_Campo
from .models.formularios.form_elemento import Form_Elemento
from .models.formularios.form_filtro_param_sort import Form_Filtro_Params_Sorteable
from .models.formularios.form_filtro_param import Form_Filtro_Param
from .models.formularios.form_filtro import Form_Filtro
from .models.formularios.form_formularios import Form_Formulario
from .models.formularios.form_imagen import Form_Imagen
from .models.formularios.form_multi_sort import Form_Multi_Options_Sorteable
from .models.formularios.form_multi import Form_Multi_Option
from .models.formularios.form_texto import Form_Texto

from .models.solicitudes.solicitud import (Solicitud)
from .models.solicitudes.solicitud_campo import Solicitud_Campo, Solicitud_Campo_Tipo


# docker exec -ti mayan-app-1 /opt/mayan-edms/bin/mayan-edms.py appearance_prepare_static 

# SOLICITUDES
admin.site.register(Solicitud)
admin.site.register(Solicitud_Campo)
admin.site.register(Solicitud_Campo_Tipo)

# PERMISOS
admin.site.register(PermisosUNQ)

# FORMULARIOS
class Campo_Inline(SortableStackedInline):
    model = Form_Campo_Sorteable
    extra = 0
    fields = ('field', 'text', 'image', ('file','form_error','form_message', 'form_same_line'), 'action')

class Accion_Inline(SortableStackedInline):
    model = Form_Accion_Sorteable
    extra = 0
    fields = ('elemento', 'accion')

class Multi_Options_Inline(SortableStackedInline):
    model = Form_Multi_Options_Sorteable
    extra = 0
    fields = ('clave', 'valor')

class Filtro_Params_Inline(SortableStackedInline):
    model = Form_Filtro_Params_Sorteable
    extra = 0
    fields = ('clave', 'valor')

class Form_Admin(NonSortableParentAdmin):
    inlines = [Campo_Inline]

class Form_Accion_Admin(NonSortableParentAdmin):
    inlines = [Accion_Inline]


class Form_Multi_Options_Admin(NonSortableParentAdmin):
    inlines = [Multi_Options_Inline]

class Form_Filtro_Param_Admin(NonSortableParentAdmin):
    inlines = [Filtro_Params_Inline]

admin.site.register(Form_Formulario, Form_Admin)

admin.site.register(Form_Accion, Form_Accion_Admin)

admin.site.register(Form_Multi_Option, Form_Multi_Options_Admin)

admin.site.register(Form_Filtro_Param, Form_Filtro_Param_Admin)

@admin.register(Form_Imagen)
class Imagen_Admin(admin.ModelAdmin):
    list_display = ('identificador', 'ruta')

@admin.register(Form_Texto)
class Texto_Admin(admin.ModelAdmin):
    list_display = ('texto', 'etiqueta')

@admin.register(Form_Elemento)
class Elemento_Admin(admin.ModelAdmin):
    list_display = ('tipo', 'readonly')

@admin.register(Form_Campo)
class Campo_Admin(admin.ModelAdmin):
    list_display = ('key', 'label', 'elemento_html', 'filtro')

@admin.register(Form_Filtro)
class Filtro_Admin(admin.ModelAdmin):
    list_display = ('tipo', 'valor')



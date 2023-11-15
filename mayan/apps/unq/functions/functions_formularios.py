import logging

from ..models.formularios.form_accion_sort import Form_Accion_Sorteable
from ..models.formularios.form_campo import Form_Campo
from ..models.formularios.form_campo_sort import Form_Campo_Sorteable
from ..models.formularios.form_elemento import Form_Elemento
from ..models.formularios.form_filtro_param_sort import Form_Filtro_Params_Sorteable
from ..models.formularios.form_filtro_param import Form_Filtro_Param
from ..models.formularios.form_filtro import Form_Filtro
from ..models.formularios.form_formularios import Form_Formulario
from ..models.formularios.form_imagen import Form_Imagen
from ..models.formularios.form_multi import Form_Multi_Option
from ..models.formularios.form_multi_sort import Form_Multi_Options_Sorteable
from ..models.formularios.form_texto import Form_Texto


logger = logging.getLogger(name=__name__)

##################################################################################
# OBTENER FORM
##################################################################################
def obtener_form(solicitud, post=None, files=None, initial=False):

    try:
        instancia = Form_Formulario.objects.get(solicitud = solicitud)

        form = form_to_dict(instancia) 

        return form
        
    except Exception as e:
        logger.error(e)
        return "No se encontro el formulario especificado"
    

##################################################################################
# GENERA EL FORMATO DE LOS DATOS EN LOS CAMPOS QUE SE PUEDEN SORTEAR
##################################################################################
def get_datos_campos_sorteable(modelo, valor):
    options_sort = modelo.objects.filter(form_id = valor.id)

    dict_base= {}
    
    if not options_sort:
        return []
    else:
        for multi in options_sort:
            dict_base.update({ multi.clave : multi.valor })
        return dict_base
    

##################################################################################
# OBTIENE LA CLAVE SEGUN EL TIPO 
##################################################################################
def get_clave_tipo(tipo, text, image):
    if tipo == 'Texto':
        return f'texto_{text}'
    elif tipo == 'Imagen':
        return f'imagen_{image}'
    else:
        return False


##################################################################################
# FORMATEA EL FORMULARIO PARA QUE SEA UN DICT PASABLE A JSON
##################################################################################
def form_to_dict(instancia : Form_Formulario):
   
    form = {}

    campos_sort = Form_Campo_Sorteable.objects.filter(form_id = instancia.id)

    count_text = 0

    count_image = 0

    for campo_sort in campos_sort:
    
        tipo = campo_sort.get_type()

        #####################################################
        # CHEQUEAMOS SI ALGUN CAMPO TIENE MAS DE UNA OPCION
        #####################################################
        if tipo == 'Error':
            return "Uno de los campos sorteables tiene seleccionado mas de un tipo, solo aceptan una opcion"

        #####################################################
        # CHEQUEAMOS SI ALGUN CAMPO ESTA TODO VACIO
        #####################################################
        elif tipo == 'None':
            return "Uno de los campos sorteables esta completamente vacio, eligale una opcion"

        #####################################################
        # CARGAMOS EL TEXTO
        #####################################################
        elif tipo == 'Texto':

            count_text += 1

            obj_texto = Form_Texto.objects.get(id = campo_sort.text_id)

            dict_text = {}
      
            for elemento in obj_texto._meta.get_fields():
                if elemento.name != 'form_campo_sorteable' and elemento.name != 'id':
                    valor = getattr(obj_texto, elemento.name)
                    dict_text.update( { elemento.name : valor } )

            dict_text["elemento_html"] = {"tipo": "text"}
            dict_text["filtro"] = 8

            form.update( { f"texto_{count_text}" : dict_text } )

        #####################################################
        # CARGAMOS EL IMAGEN
        #####################################################
        elif tipo == 'Imagen':

            count_image += 1

            obj_imagen = Form_Imagen.objects.get(id = campo_sort.image_id)

            dict_imagen = {}
      
            for elemento in obj_imagen._meta.get_fields():
                if elemento.name != 'form_campo_sorteable' and elemento.name != 'id':
                    valor = getattr(obj_imagen, elemento.name)
                    dict_imagen.update( { elemento.name : valor } )
      
            dict_imagen["elemento_html"] = {"tipo": "text"}
            dict_imagen["filtro"] = 8

            form.update( { f"imagen_{count_image}" : dict_imagen } )

        #####################################################
        # CARGAMOS EL ELEMENTO
        #####################################################
        elif tipo == 'Campo':

            obj_campo = Form_Campo.objects.get(id = campo_sort.field_id)

            dict_campo = {}
            
            for elemento in obj_campo._meta.get_fields():
                if elemento.name != 'form_campo_sorteable' and elemento.name != 'id' and elemento.name != 'key':

                    valor = getattr(obj_campo, elemento.name) 
                    
                    if isinstance(valor, Form_Elemento):
                        dict_campo.update( { elemento.name : valor.get_dict()})

                    elif isinstance(valor, Form_Filtro):
                        dict_campo.update( { elemento.name : valor.get_valor()})

                    elif isinstance(valor, Form_Filtro_Param):

                        res = get_datos_campos_sorteable(Form_Filtro_Params_Sorteable, valor)

                        dict_campo.update( { elemento.name : res } )

                    elif isinstance(valor, Form_Multi_Option):
                        
                        res = get_datos_campos_sorteable(Form_Multi_Options_Sorteable, valor)
                            
                        dict_campo.update( { elemento.name : res } )

                    elif valor is not None:
                        dict_campo.update( { elemento.name : valor } )

            form.update( { obj_campo.key : dict_campo } )

        #####################################################
        # CARGAMOS ARCHIVO
        #####################################################
        if campo_sort.file == True:
            clave = get_clave_tipo(tipo, count_text, count_image)
            if clave :
                form[clave].update( { "archivo" : True } )
            else:
                form[obj_campo.key].update( {"archivo" : True } )

        #####################################################
        # CARGAMOS FORM ERROR
        #####################################################
        if campo_sort.form_error == True:
            clave = get_clave_tipo(tipo, count_text, count_image)
            if clave :
                form[clave].update( { "form_error" : True } )
            else:
                form[obj_campo.key].update( {"form_error" : True } )

        #####################################################
        # CARGAMOS FORM MENSAJE
        #####################################################
        if campo_sort.form_message == True:
            clave = get_clave_tipo(tipo, count_text, count_image)
            if clave :
                form[clave].update( { "form_message" : True } )
            else:
                form[obj_campo.key].update( {"form_message" : True } )

        #####################################################
        # CARGAMOS MISMA LINEA QUE ELEMENTO ANTERIOR
        #####################################################
        if campo_sort.form_same_line:
            clave = get_clave_tipo(tipo, count_text, count_image)
            if clave :
                form[clave].update( { "form_same_line" : campo_sort.form_same_line } )
            else:
                form[obj_campo.key].update( {"form_same_line" : campo_sort.form_same_line } )
            
        #####################################################
        # CARGAMOS ACCIONES
        #####################################################
        if campo_sort.get_action():
            acciones_sort = Form_Accion_Sorteable.objects.filter(form_id = campo_sort.action_id)

            dict_act = {}

            for act in acciones_sort:
                dict_act.update( { act.elemento : act.accion } ) 
        
            clave = get_clave_tipo(tipo, count_text, count_image)
            if clave :
                form[clave].update( { "acciones" : dict_act } )
            else:
                form[obj_campo.key].update( {"acciones" : dict_act } )
            

    return form
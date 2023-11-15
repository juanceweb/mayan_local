import logging

from mayan.apps.rest_api import generics

from django.http import JsonResponse

from ..functions.functions_formularios import obtener_form

logger = logging.getLogger(name=__name__)

##################################################################################
# Controlador API unq/solicitudes_form/{solicitud}
##################################################################################
class APIFormView(generics.GenericAPIView):
    """
    GET : Devuelve el FORMULARIO en base a la solicitud que se le pasa
    """

    def get(self, request,format=None, *args, **kwargs):

        solicitud = kwargs['solicitud']

        form = obtener_form(solicitud, initial= {'solicitud': solicitud } )

        return JsonResponse( {'form': form } )
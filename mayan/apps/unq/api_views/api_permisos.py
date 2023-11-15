import logging

from mayan.apps.rest_api import generics

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from ...document_states.models.workflow_instance_models import WorkflowInstance
from ..models.permisos.permisos import PermisosUNQ

logger = logging.getLogger(name=__name__)


##################################################################################
# Controlador API unq/groups/permisos/{document_id}
##################################################################################
class APIUNQGroupsPermisosView(generics.GenericAPIView):
    """
    GET : Devuelve los GRUPOS con los que se puede comunicar cada GRUPO (a los que pertenece el usuario) en determinado WORKFLOW STATE
    """

    def get(self, request,format=None, *args, **kwargs):

        permisos = {}

        try:
            # CHEQUEA SI LA INSTANCIA DE WORKFLOW ENVIADA EXISTE
            workflow_instance = WorkflowInstance.objects.get(document_id = kwargs["document_id"])

        except ObjectDoesNotExist:
            return JsonResponse( {"error" : "no se encontro instancia de workflow asociada a ese id" } )
        
        try:
            # OBTIENE EL WORKFLOW STATE ACTUAL DE LA SOLICITUD
            current_state = workflow_instance.get_current_state()

            # OBTIENE LOS PERMISOS DE ESE WORKFLOW STATE
            state = PermisosUNQ.objects.get(workflow_state_id = current_state.id)
            
            for grupo, permiso in state.permisos.items():
                permisos.update({grupo : permiso})

            # OBTIENE LOS GRUPOS A LOS QUE PERTENECE EL USUARIO
            user_groups = request.user.groups.all().values("name")
            user_groups_list = [group["name"] for group in user_groups]

            permisos_final = []

            # ARMA LOS GRUPOS CON LOS QUE SE PUEDE COMUNICAR EN BASE A CADA GRUPO DEL USUARIO
            for group in user_groups_list:
                if group in permisos:
                    permisos_final.extend(permisos[group])

            permisos_final = list(set(permisos_final))

            return JsonResponse( { "permisos" : permisos_final } )
        
        except ObjectDoesNotExist:
            return JsonResponse( {"permisos" : permisos } )


##################################################################################
# Controlador API unq/groups/
##################################################################################
class APIUNQGroupsView(generics.GenericAPIView):
    """
    GET : Devuelve una lista con los ID, de los GRUPOS a los que el USUARIO pertenece
    """

    def get(self, request,format=None, *args, **kwargs):

        user_groups = request.user.groups.all().values("name")

        user_group_list = [group["name"] for group in user_groups]

        return JsonResponse( { "grupos" : user_group_list } )


import logging
from ..models.permisos.permisos import PermisosUNQ
from ...permissions.models import Role

logger = logging.getLogger(name=__name__)

def generar_permisos(state_id):
    try:
        obj_permisos = PermisosUNQ.objects.get(workflow_state_id = state_id)
        return obj_permisos.permisos
    except:
        logger.error("El estado no tiene permisos asignados")
        return {}
    
    
def generar_roles(user_groups):
    groups_id = []

    for group in user_groups:
        groups_id.append(group.id)

    # SI NO TIENE GRUPO, NO TIENE UN ROL
    if groups_id:

        groups_roles = []

        # AGARRAMOS LOS ROLES ASOCIADOS AL GRUPO
        for group_id in groups_id:

            roles = Role.objects.filter(groups= group_id )

            for rol in roles:
                groups_roles.append(rol.label)

        if groups_roles:
            return groups_roles
        else:
            return []

    else:
        return []

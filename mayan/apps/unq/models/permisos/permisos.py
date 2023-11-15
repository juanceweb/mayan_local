
from django.db import models
from django.utils.translation import ugettext_lazy as _

from smart_selects.db_fields import ChainedForeignKey

from ....document_states.models.workflow_models import Workflow
from ....document_states.models.workflow_state_models import WorkflowState

class PermisosUNQ(models.Model):

    workflow = models.ForeignKey(null=True, on_delete=models.CASCADE, to=Workflow,
        verbose_name=_('Workflow'))
    
    workflow_state = ChainedForeignKey(
        WorkflowState,
        chained_field="workflow",
        chained_model_field="workflow",
        show_all=False,
        auto_choose=False,
        sort=False)
    
    permisos = models.JSONField()

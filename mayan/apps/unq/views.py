import logging
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from .models.permisos.permisos import PermisosUNQ
from ..document_states.models.workflow_state_models import WorkflowState
from ..document_states.models.workflow_models import Workflow
from django.contrib.auth.models import Group
from .forms.form_permisos import PermisosUNQForm

logger = logging.getLogger(name=__name__)


##################################################################################
# Controlador BACK unq/permisos
##################################################################################
def permisos_unq_form(request):

    if request.method == 'POST':

        form = PermisosUNQForm(request.POST)

        if form.is_valid():
            
            # copiamos la request para poder trabajarla
            nueva_request = request.POST.copy()

            # sacamos los datos que no queremos recorrer
            nueva_request.pop('csrfmiddlewaretoken')
            workflow = nueva_request.pop('workflow')
            workflow_state = nueva_request.pop('workflow_state')

            permisos_json = {}

            for elem in nueva_request:
                permisos_json[elem] = nueva_request.getlist(elem)


            # buscamos el workflow y el estate por el id que estaba en la request
            par_workflow = Workflow.objects.get(id = workflow[0])
            par_workflow_state = WorkflowState.objects.get(id=workflow_state[0])
            par_permisos = permisos_json

            PermisosUNQ.objects.create(workflow=par_workflow, workflow_state=par_workflow_state, permisos=par_permisos )

            return redirect('/unq/permisos/list')

        else:
            grupos = Group.objects.values("name")

            return render(request, template_name='unq/permisosunq_form.html', context= {'form': form, 'grupos': grupos })


    else:
        form = PermisosUNQForm()
        
        grupos = Group.objects.values("name")
 
        return render(request, template_name='unq/permisosunq_form.html', context= {'form': form, 'grupos': grupos })

    
##################################################################################
# Controlador BACK unq/permisos/list
##################################################################################
class PermisosUNQListView(ListView):
    model = PermisosUNQ



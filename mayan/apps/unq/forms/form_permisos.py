from django import forms
from ..models.permisos.permisos import PermisosUNQ


class PermisosUNQForm(forms.ModelForm):

    class Meta:
        model = PermisosUNQ
        fields = ['workflow', 'workflow_state']
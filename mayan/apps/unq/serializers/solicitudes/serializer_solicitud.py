from django.utils.translation import ugettext_lazy as _

from mayan.apps.rest_api import serializers
from mayan.apps.user_management.serializers import UserSerializer

from ...models.solicitudes.solicitud import Solicitud

##################################################################################
# SERIALIZER SOLICITUD
##################################################################################
class Solicitud_Serializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(read_only=True)
   
    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'document_id',
                'view_name': 'rest_api:document-detail'
            },
        }
        model = Solicitud
        fields = '__all__'
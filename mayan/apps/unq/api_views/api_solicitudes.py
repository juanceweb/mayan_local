import logging

from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from mayan.apps.acls.models import AccessControlList
from mayan.apps.permissions.models import Role
from mayan.apps.rest_api import generics

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import JsonResponse

from ...documents.models.document_models import Document
from ...documents.models.document_type_models import DocumentType
from ...documents.models.document_file_models import DocumentFile
from ...documents.api_views.document_file_api_views import APIDocumentFileListView
from ...documents.api_views.document_api_views import APIDocumentListView, APIDocumentUploadView, APIDocumentDetailView

from ...document_comments.api_views import APICommentListView
from ...document_comments.permissions import permission_document_comment_create

from ...acls.models import AccessControlList
from ...document_states.api_views.workflow_instance_api_views import APIWorkflowInstanceLogEntryListView

from ...documents.permissions import (
    permission_document_create, permission_document_view, permission_document_file_new, permission_document_file_delete
)

from ..functions.functions_solicitudes import json_tutores, json_docentes
from ..models.solicitudes.solicitud_campo import Solicitud_Campo
from ..models.solicitudes.solicitud import Solicitud

logger = logging.getLogger(name=__name__)

    
def get_query_por_role(queryset, permission, role, user):
            
    content_type = ContentType.objects.get_for_model(model=queryset.model)

    acl_filters = AccessControlList.objects.filter(content_type=content_type, permissions=permission.stored_permission, role=role.id).values('object_id')
    
    field_lookup = 'id__in'

    result = []

    result.append(
            Q(
                **{field_lookup: acl_filters}
            )
        )

    final_query = None
    for acl_filter in result:
        if final_query is None:
            final_query = acl_filter
        else:
            final_query = final_query | acl_filter

    new_queryset = queryset.filter(final_query)

    # SI EL ROLE ES EL DEL SOLICITANTE, FILTRA POR SOLO LOS CREADOS POR EL USUARIO
    if role.id == 5:
        queryset_solicitante = []

        for doc in new_queryset:
            if doc.solicitud.user.id == user.id:
                queryset_solicitante.append(doc)

        lista_ids = [objeto.id for objeto in queryset_solicitante]
        
        new_queryset = new_queryset.filter(id__in=lista_ids)

    return new_queryset


##################################################################################
# Controlador API unq/documents/list/{filtro}
##################################################################################
class APIUNQDocumentListView(APIDocumentListView):
    """
    get: obtiene la lista de documentos
    post: crea un nuevo documento sin archivo
    """

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        if int(kwargs["filtro"]):
            queryset= queryset.filter(document_type__id = int(kwargs["filtro"]))

        user_groups = request.user.groups.all()

        if len(user_groups) > 1:

            permiso = permission_document_view

            final_query = {}

            for group in user_groups:
                role = Role.objects.get(groups = group.id)
                
                new_query = get_query_por_role(queryset, permiso, role, request.user)

                serializer = self.get_serializer(new_query, many=True)

                final_query.update({group.name : serializer.data})

            return Response( { "results_varios" : final_query } )

        else:
            group_id = user_groups[0].id

            if group_id == 5:
                queryset_solicitante = []

                for doc in queryset:
                    if doc.solicitud.user.id == request.user.id:
                        queryset_solicitante.append(doc)
                
                queryset = queryset_solicitante

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)

                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, request):

        queryset = DocumentType.objects.all()

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_create, queryset=queryset,
            user=self.request.user
        )

        serializer.validated_data['document_type'] = get_object_or_404(
            pk=serializer.validated_data['document_type_id'],
            queryset=queryset
        )

        solicitud = Solicitud.objects.create(user_id = request.user.id)

        tutores_index = 0
        docentes_index = 0

        for campo, valor in serializer.initial_data.items():
            if campo == "document_type_id":
                pass
            elif campo[:7] == "tutores":
                if tutores_index == 0:
                    Solicitud_Campo.objects.create(solicitud_id=solicitud.id,nombre_campo="tutores", valor_campo=json_tutores(serializer.initial_data))
                    tutores_index +=1
            elif campo[:8] == "docentes":
                if docentes_index == 0:
                    Solicitud_Campo.objects.create(solicitud_id=solicitud.id,nombre_campo="docentes", valor_campo=json_docentes(serializer.initial_data))
                    docentes_index +=1
            else:
                Solicitud_Campo.objects.create(solicitud_id=solicitud.id, nombre_campo=campo, valor_campo=valor)

        serializer.validated_data['solicitud'] = solicitud

        super().perform_create(serializer=serializer)


##################################################################################
# Controlador API /unq/documents/upload
##################################################################################
class APIUNQDocumentUploadView(APIDocumentUploadView):
    """
    post: crea un nuevo documento + archivo
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, request):
        queryset = DocumentType.objects.all()

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_create, queryset=queryset,
            user=self.request.user
        )

        serializer.validated_data['document_type'] = get_object_or_404(
            pk=serializer.validated_data['document_type_id'],
            queryset=queryset
        )

        solicitud = Solicitud.objects.create(user_id = request.user.id)

        tutores_index = 0
        docentes_index = 0

        for campo, valor in serializer.initial_data.items():
            if campo == "document_type_id" or campo == "file":
                pass
            elif campo[:7] == "tutores":
                if tutores_index == 0:
                    Solicitud_Campo.objects.create(solicitud_id=solicitud.id,nombre_campo="tutores", valor_campo=json_tutores(serializer.initial_data))
                    tutores_index +=1
            elif campo[:8] == "docentes":
                if docentes_index == 0:
                    Solicitud_Campo.objects.create(solicitud_id=solicitud.id,nombre_campo="docentes", valor_campo=json_docentes(serializer.initial_data))
                    docentes_index +=1
            else:
                Solicitud_Campo.objects.create(solicitud_id=solicitud.id, nombre_campo=campo, valor_campo=valor)

        serializer.validated_data['solicitud'] = solicitud

        super().perform_create(serializer=serializer)


##################################################################################
# Controlador API unq/documents/{document_id}/
##################################################################################
class APIUNQDocumentDetailView(APIDocumentDetailView):

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        user_groups = self.request.user.groups.all()

        if len(user_groups) > 1:

            permiso = permission_document_view

            final_query = set()

            for group in user_groups:
                role = Role.objects.get(groups = group.id)
                
                new_query = get_query_por_role(queryset, permiso, role, self.request.user)

                final_query.update(new_query)

            lista_ids = [objeto.id for objeto in final_query]

            queryset = queryset.filter(id__in=lista_ids)

        else:
            group_id = user_groups[0].id

            if group_id == 5:
                queryset_solicitante = []

                for doc in queryset:
                    if doc.solicitud.user.id == self.request.user.id:
                        queryset_solicitante.append(doc)
                
                lista_ids = [objeto.id for objeto in queryset_solicitante]

                queryset = queryset.filter(id__in=lista_ids)

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


##################################################################################
# Controlador API unq/documents/{document_id}/comments/{group}
##################################################################################
class APIUNQCommentListView(APICommentListView):

# CHEQUEA SI EL USUARIO TIENE PERMISOS PARA VER LOS MENSAJES CON LOS GRUPOS A LOS QUE PERTECENE    
    def get_external_object_queryset_filtered(self):
        queryset = self.get_external_object_queryset()
        permission = self.get_external_object_permission()

        user_groups = self.request.user.groups.all()

        if len(user_groups) > 1:

            final_query = set()

            for group in user_groups:

                role = Role.objects.get(groups = group.id)
                
                new_query = get_query_por_role(queryset, permission, role, self.request.user)

                final_query.update(new_query)

            lista_ids = [objeto.id for objeto in final_query]

            queryset = queryset.filter(id__in=lista_ids)

        else:
            group_id = user_groups[0].id
                
            role = Role.objects.get(groups = group_id)

            permission = self.get_external_object_permission()
            
            new_query = get_query_por_role(queryset, permission, role, self.request.user)

            queryset = new_query 

        return queryset
    
# LISTA LOS MENSAJES QUE PUEDE VER EL USUARIO CON EL GRUPO EN SESION EN AUTOGESTION
    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
            
        try:
            group = request.user.groups.all().get(name= kwargs["group"])
        except:
            return Response(f"El usuario no tiene el rol {kwargs['role']}")
        
        new_queryset = []

        for comment in queryset:

            if comment.user.id == request.user.id:
                new_queryset.append(comment)
            else:
                if group.name in comment.grupo_destino:
                    new_queryset.append(comment)
                elif comment.grupo_destino == []:
                    new_queryset.append(comment)

        page = self.paginate_queryset(new_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(new_queryset, many=True)
        return Response(serializer.data)

# CREA EL MENSAJE, CON DESTINATARIO PASADO Y EL GRUPO EN SESION EN AUTOGESTION
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if "grupo_destino" in serializer.validated_data:
            serializer.validated_data["grupo_destino"].append(kwargs["group"])         

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

##################################################################################
# Controlador API unq/documents/{document_id}/files/{group}
##################################################################################
class APIUNQDocumentFileListView(APIDocumentFileListView):

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
            
        try:
            group = request.user.groups.all().get(name= kwargs["group"])
        except:
            return Response(f"El usuario no tiene el rol {kwargs['role']}")
        
        new_queryset = []

        for file in queryset:

            if file.comment != "":

                comments_array = file.comment.split()

                if group.name in comments_array:
                    new_queryset.append(file)
            
            else:
                new_queryset.append(file)

        page = self.paginate_queryset(new_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(new_queryset, many=True)
        return Response(serializer.data)

    def get_document(self, permission=None):
        queryset = self.get_document_queryset()

        user_groups = self.request.user.groups.all()

        if len(user_groups) > 1:

            final_query = set()

            for group in user_groups:

                role = Role.objects.get(groups = group.id)
                
                new_query = get_query_por_role(queryset, permission, role, self.request.user)

                final_query.update(new_query)

            lista_ids = [objeto.id for objeto in final_query]

            queryset = queryset.filter(id__in=lista_ids)

        else:
            group_id = user_groups[0].id

            role = Role.objects.get(groups = group_id)
                
            new_query = get_query_por_role(queryset, permission, role, self.request.user)

            queryset = new_query 

        return get_object_or_404(
            queryset=queryset, pk=self.kwargs['document_id']
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if 'comment' in serializer.validated_data:
            serializer.validated_data["comment"] += " " + kwargs["group"]
        
        self.perform_create(serializer)

        return Response(status=status.HTTP_202_ACCEPTED)
            

##################################################################################
# Controlador API unq/documents/files/{file_id}
##################################################################################
class APIUNQFileDeleteView(generics.GenericAPIView):

    def post(self, request,format=None, *args, **kwargs):

        try:
            
            file = DocumentFile.objects.get(id=kwargs["file_id"])

            file.comment = "desestimado"
            file.filename = "desestimado"

            file.save()

            return Response(True)
        except:
            return Response("el file id no existe")



##################################################################################
# Controlador API unq/documents/{document_id}/workflow_instances/{workflow_id}/log_entries
##################################################################################
class APIUNQWorkflowInstanceLogEntryListView(APIWorkflowInstanceLogEntryListView):
    
      def get_external_object_queryset_filtered(self):
        queryset = self.get_external_object_queryset()
        permission = self.get_external_object_permission()

        user_groups = self.request.user.groups.all()

        if len(user_groups) > 1:

            final_query = set()

            for group in user_groups:

                role = Role.objects.get(groups = group.id)

                permission = permission_document_view
                
                new_query = get_query_por_role(queryset, permission, role, self.request.user)

                final_query.update(new_query)

            lista_ids = [objeto.id for objeto in final_query]

            queryset = queryset.filter(id__in=lista_ids)

        else:
            group_id = user_groups[0].id

            role = Role.objects.get(groups = group_id)
                
            new_query = get_query_por_role(queryset, permission, role, self.request.user)

            queryset = new_query 

        return queryset
      

##################################################################################
# Controlador API unq/documents/{document_id}/permisos/
##################################################################################
class APIUNQCommentsPermisoView(generics.GenericAPIView):

    def post(self, request,format=None, *args, **kwargs):
        
        queryset = Document.objects.filter(id=kwargs["document_id"])

        role = request.POST.get("role", False)
        permiso = request.POST.get("permiso", False)

        if not role:
            return JsonResponse({"role": ["Este campo es requerido."] } )
        
        if not permiso:
            return JsonResponse({"permiso": ["Este campo es requerido."] } )
        
        if permiso == "comment_create":
            permiso = permission_document_comment_create
        elif permiso == "file_create":
            permiso = permission_document_file_new
        elif permiso == "file_delete":
            permiso = permission_document_file_delete
        else:
            return Response(False)
             
        try:
            group = request.user.groups.all().get(name= role)
        except:
            return Response(False)
        
        role = Role.objects.get(groups = group.id)

        new_query = get_query_por_role(queryset, permiso, role, self.request.user)

        queryset = new_query 

        if queryset:
            return Response(True)
        else:
            return Response(False)
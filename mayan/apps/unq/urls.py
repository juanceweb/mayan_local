from django.conf.urls import url
from .api_views.api_formularios import APIFormView
from .api_views.api_permisos import APIUNQGroupsView, APIUNQGroupsPermisosView
from .api_views.api_solicitudes import (APIUNQDocumentListView, APIUNQDocumentUploadView, 
        APIUNQDocumentDetailView, APIUNQCommentListView, APIUNQWorkflowInstanceLogEntryListView, 
        APIUNQCommentsPermisoView, APIUNQDocumentFileListView, APIUNQFileDeleteView)
from .views import PermisosUNQListView, permisos_unq_form

urlpatterns_permisos_unq = [
    url(
        regex=r'^permisos/$',
        name='unq-permisos', view=permisos_unq_form
    ),
    url(
        regex=r'^permisos/list$',
        name='unq-permisos-list', view=PermisosUNQListView.as_view()
    ),
]

urlpatterns = []
urlpatterns.extend(urlpatterns_permisos_unq)

api_urls_formularios = [
    url(
        regex=r'^unq/formularios/(?P<solicitud>\w+)/$', name='unq-formularios',
        view=APIFormView.as_view()
    )
]

api_urls_grupos = [
    url(
        regex=r'^unq/groups/$', name='unq-groups',
        view=APIUNQGroupsView.as_view()
    ),
    url(
        regex=r'^unq/groups/permisos/(?P<document_id>[0-9]+)$', name='unq-groups-permisos-document',
        view=APIUNQGroupsPermisosView.as_view()
    )

]

api_urls_solicitudes = [
    url(
        regex=r'^unq/documents/list/(?P<filtro>[0-9]+)/$', name='unq-documents-list',
        view=APIUNQDocumentListView.as_view()
    ),
    url(
        regex=r'^unq/documents/upload/$', name='unq-documents-upload',
        view=APIUNQDocumentUploadView.as_view()
    ),
    url(
        regex=r'^unq/documents/(?P<document_id>[0-9]+)/$', name='unq-documents-detail',
        view=APIUNQDocumentDetailView.as_view()
    ),
    url(
        regex=r'^unq/documents/(?P<document_id>[0-9]+)/comments/(?P<group>\w+)/$', name='unq-documents-comments',
        view=APIUNQCommentListView.as_view()
    ),
    url(
        regex=r'^unq/documents/(?P<document_id>[0-9]+)/files/(?P<group>\w+)/$', name='unq-documents-files',
        view=APIUNQDocumentFileListView.as_view()
    ),
    url(
        regex=r'^unq/documents/files/(?P<file_id>[0-9]+)/delete/$', name='unq-files-delete',
        view=APIUNQFileDeleteView.as_view()
    ),
    url(
        regex=r'^unq/documents/(?P<document_id>[0-9]+)/workflow_instances/(?P<workflow_instance_id>[0-9]+)/log_entries/$', 
        name='unq-workflow-instance-log-entry-list',
        view=APIUNQWorkflowInstanceLogEntryListView.as_view()
    ),
    url(
        regex=r'^unq/documents/(?P<document_id>[0-9]+)/permisos/$', 
        name='unq-comment-create-permission',
        view=APIUNQCommentsPermisoView.as_view()
    )
]

api_urls = []
api_urls.extend(api_urls_formularios)
api_urls.extend(api_urls_solicitudes)
api_urls.extend(api_urls_grupos)


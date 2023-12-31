from django.utils.translation import ugettext_lazy as _

from mayan.apps.rest_api import serializers
from mayan.apps.rest_api.relations import MultiKwargHyperlinkedIdentityField

from ..models.document_file_models import DocumentFile
from ..models.document_file_page_models import DocumentFilePage

from django.contrib.postgres.fields import ArrayField


class DocumentFilePageSerializer(serializers.HyperlinkedModelSerializer):
    document_file_url = MultiKwargHyperlinkedIdentityField(
        label=_('Document file URL'), view_kwargs=(
            {
                'lookup_field': 'document_file.document.pk',
                'lookup_url_kwarg': 'document_id'
            },
            {
                'lookup_field': 'document_file_id',
                'lookup_url_kwarg': 'document_file_id'
            }
        ), view_name='rest_api:documentfile-detail'
    )
    image_url = MultiKwargHyperlinkedIdentityField(
        label=_('Image URL'), view_kwargs=(
            {
                'lookup_field': 'document_file.document.pk',
                'lookup_url_kwarg': 'document_id'
            },
            {
                'lookup_field': 'document_file_id',
                'lookup_url_kwarg': 'document_file_id'
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_file_page_id'
            }
        ), view_name='rest_api:documentfilepage-image'
    )
    url = MultiKwargHyperlinkedIdentityField(
        label=_('URL'), view_kwargs=(
            {
                'lookup_field': 'document_file.document.pk',
                'lookup_url_kwarg': 'document_id'
            },
            {
                'lookup_field': 'document_file_id',
                'lookup_url_kwarg': 'document_file_id'
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_file_page_id'
            }
        ), view_name='rest_api:documentfilepage-detail'
    )

    class Meta:
        fields = (
            'document_file_id', 'document_file_url', 'id', 'image_url',
            'page_number', 'url'
        )
        model = DocumentFilePage
        read_only_fields = (
            'document_file_id', 'document_file_url', 'id', 'image_url', 'url'
        )


class DocumentFileSerializer(serializers.HyperlinkedModelSerializer):
    action_name = serializers.CharField(
        label=_('Action name'), write_only=True
    )
    document_url = serializers.HyperlinkedIdentityField(
        label=_('Document URL'), lookup_field='document_id',
        lookup_url_kwarg='document_id', view_name='rest_api:document-detail'
    )
    download_url = MultiKwargHyperlinkedIdentityField(
        label=_('Download URL'), view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id'
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_file_id'
            }
        ), view_name='rest_api:documentfile-download'
    )
    file_new = serializers.FileField(
        help_text=_('Binary content for the new file.'),
        label=_('File new'), use_url=False, write_only=True
    )
    page_list_url = MultiKwargHyperlinkedIdentityField(
        label=_('Page list URL'), view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id'
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_file_id'
            }
        ), view_name='rest_api:documentfilepage-list'
    )
    pages_first = DocumentFilePageSerializer(
        label=_('Pages first'), many=False, read_only=True
    )
    url = MultiKwargHyperlinkedIdentityField(
        label=_('URL'), view_kwargs=(
            {
                'lookup_field': 'document_id',
                'lookup_url_kwarg': 'document_id'
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'document_file_id'
            }
        ),
        view_name='rest_api:documentfile-detail'
    )

    class Meta:
        create_only_fields = ('action_name', 'file_new',)
        extra_kwargs = {
            'file': {'use_url': False},
        }

        fields = (
            'action_name', 'checksum', 'comment', 'document_id', 'document_url',
            'download_url', 'encoding', 'file', 'file_new', 'filename', 'id',
            'mimetype', 'page_list_url', 'pages_first', 'size', 'timestamp',
            'url'
        )
        model = DocumentFile
        read_only_fields = (
            'checksum', 'document_id', 'document_url', 'download_url',
            'encoding', 'file', 'id', 'mimetype', 'page_list_url',
            'pages_first', 'size', 'timestamp', 'url'
        )



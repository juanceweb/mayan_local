from datetime import timedelta
import logging

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from mayan.apps.databases.classes import ModelQueryFields

from .settings import (
    setting_favorite_count, setting_recently_accessed_document_count,
    setting_recently_created_document_count
)

logger = logging.getLogger(name=__name__)


class DocumentManager(models.Manager):
    def get_by_natural_key(self, uuid):
        return self.get(
            uuid=str(uuid)
        )


class DocumentFileManager(models.Manager):
    def get_by_natural_key(self, checksum, document_natural_key):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        try:
            document = Document.objects.get_by_natural_key(
                *document_natural_key
            )
        except Document.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(document__pk=document.pk, checksum=checksum)


class DocumentFilePageManager(models.Manager):
    def get_by_natural_key(self, page_number, document_file_natural_key):
        DocumentFile = apps.get_model(
            app_label='documents', model_name='DocumentFile'
        )
        try:
            document_file = DocumentFile.objects.get_by_natural_key(
                *document_file_natural_key
            )
        except DocumentFile.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(
            document_file__pk=document_file.pk, page_number=page_number
        )


class DocumentTypeManager(models.Manager):
    def check_delete_periods(self):
        logger.info(msg='Executing')

        for document_type in self.all():
            logger.info(
                'Checking deletion period of document type: %s',
                document_type
            )
            if document_type.delete_time_period and document_type.delete_time_unit:
                delta = timedelta(
                    **{
                        document_type.delete_time_unit: document_type.delete_time_period
                    }
                )
                logger.info(
                    'Document type: %s, has a deletion period delta of: %s',
                    document_type, delta
                )
                for document in document_type.trashed_documents.filter(trashed_date_time__lt=now() - delta):
                    logger.info(
                        'Document "%s" with id: %d, trashed on: %s, exceeded '
                        'delete period', document, document.pk,
                        document.trashed_date_time
                    )
                    document.delete()
            else:
                logger.info(
                    'Document type: %s, has a no retention delta',
                    document_type
                )

        logger.info(msg='Finished')

    def check_trash_periods(self):
        logger.info(msg='Executing')

        for document_type in self.all():
            logger.info(
                'Checking trash period of document type: %s', document_type
            )
            if document_type.trash_time_period and document_type.trash_time_unit:
                delta = timedelta(
                    **{
                        document_type.trash_time_unit: document_type.trash_time_period
                    }
                )
                logger.info(
                    'Document type: %s, has a trash period delta of: %s',
                    document_type, delta
                )
                for document in document_type.documents.filter(datetime_created__lt=now() - delta):
                    logger.info(
                        'Document "%s" with id: %d, added on: %s, exceeded '
                        'trash period', document, document.pk,
                        document.datetime_created
                    )
                    document.delete()
            else:
                logger.info(
                    'Document type: %s, has a no retention delta',
                    document_type
                )

        logger.info(msg='Finished')

    def document_stubs_delete(self):
        logger.info(msg='Executing')

        for document_type in self.all():
            logger.info(
                'Checking expired document stubs of document type: %s',
                document_type
            )

            if document_type.document_stub_pruning_enabled:
                stale_stub_documents = document_type.documents.filter(
                    is_stub=True, datetime_created__lt=now() - timedelta(
                        seconds=document_type.document_stub_expiration_interval
                    )
                )
                logger.debug(
                    'Deleting %d document stubs', stale_stub_documents.count()
                )
                for stale_stub_document in stale_stub_documents:
                    stale_stub_document.delete(to_trash=False)

        logger.info(msg='Finished')

    def get_by_natural_key(self, label):
        return self.get(label=label)


class FavoriteDocumentManager(models.Manager):
    def get_by_natural_key(
        self, datetime_accessed, document_natural_key, user_natural_key
    ):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        User = get_user_model()
        try:
            document = Document.objects.get_by_natural_key(
                *document_natural_key
            )
        except Document.DoesNotExist:
            raise self.model.DoesNotExist
        else:
            try:
                user = User.objects.get_by_natural_key(*user_natural_key)
            except User.DoesNotExist:
                raise self.model.DoesNotExist

        return self.get(document__pk=document.pk, user__pk=user.pk)


class RecentlyAccessedDocumentManager(models.Manager):
    def get_by_natural_key(
        self, datetime_accessed, document_natural_key, user_natural_key
    ):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        User = get_user_model()
        try:
            document = Document.objects.get_by_natural_key(
                *document_natural_key
            )
        except Document.DoesNotExist:
            raise self.model.DoesNotExist
        else:
            try:
                user = User.objects.get_by_natural_key(*user_natural_key)
            except User.DoesNotExist:
                raise self.model.DoesNotExist

        return self.get(
            document__pk=document.pk, user__pk=user.pk,
            datetime_accessed=datetime_accessed
        )


class TrashCanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_trash=True)


class TrashCanQuerySet(models.QuerySet):
    def delete(self, to_trash=True):
        for instance in self:
            instance.delete(to_trash=to_trash)


class ValidDocumentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            in_trash=False
        )


class ValidDocumentFileManager(models.Manager):
    def get_queryset(self):
        return models.QuerySet(
            model=self.model, using=self._db
        ).filter(document__in_trash=False)


class ValidDocumentFilePageManager(models.Manager):
    def get_queryset(self):
        return models.QuerySet(
            model=self.model, using=self._db
        ).filter(
            document_file__document__in_trash=False
        )


class ValidDocumentVersionManager(models.Manager):
    def get_queryset(self):
        return models.QuerySet(
            model=self.model, using=self._db
        ).filter(document__in_trash=False)


class ValidDocumentVersionPageManager(models.Manager):
    def get_queryset(self):
        return models.QuerySet(
            model=self.model, using=self._db
        ).filter(
            document_version__document__in_trash=False
        )


class ValidFavoriteDocumentManager(models.Manager):
    def add_for_user(self, user, document):
        favorite_document, created = self.model.objects.get_or_create(
            user=user, document=document
        )

        # Delete old (by date) favorites in excess of the values of
        # setting_favorite_count.
        favorites_to_delete = self.filter(user=user).values('pk').order_by(
            '-datetime_added'
        )[setting_favorite_count.value:]
        self.filter(pk__in=favorites_to_delete).delete()

        return favorite_document

    def get_for_user(self, user):
        FavoriteDocumentProxy = apps.get_model(
            app_label='documents', model_name='FavoriteDocumentProxy'
        )

        if user.is_authenticated:
            return FavoriteDocumentProxy.valid.filter(favorites__user=user)
        else:
            return FavoriteDocumentProxy.valid.none()

    def get_queryset(self):
        return super().get_queryset().filter(
            document__in_trash=False
        )

    def remove_for_user(self, user, document):
        self.get(user=user, document=document).delete()


class ValidFavoriteDocumentProxyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            in_trash=False
        )


class ValidRecentlyAccessedDocumentManager(models.Manager):
    def add_document_for_user(self, user, document):
        if user.is_authenticated:
            new_recent, created = self.model.objects.get_or_create(
                user=user, document=document
            )
            if not created:
                # Document already in the recent list, just save to force
                # accessed date and time update.
                new_recent.save(
                    update_fields=('datetime_accessed',)
                )

            recent_to_delete = self.filter(user=user).values_list(
                'pk', flat=True
            )[
                setting_recently_accessed_document_count.value:
            ]

            self.filter(
                pk__in=list(recent_to_delete)
            ).delete()
        return new_recent

    def get_for_user(self, user):
        RecentlyAccessedDocumentProxy = apps.get_model(
            app_label='documents', model_name='RecentlyAccessedDocumentProxy'
        )

        if user.is_authenticated:
            return RecentlyAccessedDocumentProxy.valid.filter(
                recent__user=user
            ).order_by('-recent__datetime_accessed')
        else:
            return RecentlyAccessedDocumentProxy.objects.none()

    def get_queryset(self):
        return super().get_queryset().filter(
            document__in_trash=False
        )


class ValidRecentlyCreatedDocumentManager(models.Manager):
    def get_queryset(self):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        queryset = ModelQueryFields.get(
            model=Document
        ).get_queryset(manager_name='valid')

        return super().get_queryset().filter(
            pk__in=queryset.order_by('-datetime_created')[
                :setting_recently_created_document_count.value
            ].values('pk')
        ).order_by('-datetime_created')

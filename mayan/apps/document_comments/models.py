from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.documents.models.document_models import Document
from mayan.apps.events.decorators import method_event
from mayan.apps.events.event_managers import (
    EventManagerMethodAfter, EventManagerSave
)

from .events import (
    event_document_comment_created, event_document_comment_deleted,
    event_document_comment_edited
)
from .model_mixins import CommentBusinessLogicMixin


class Comment(CommentBusinessLogicMixin, ExtraDataModelMixin, models.Model):
    """
    Model to store one comment per document per user per date & time.
    """
    _event_created_event = event_document_comment_created
    _event_edited_event = event_document_comment_created

    document = models.ForeignKey(
        db_index=True, on_delete=models.CASCADE, related_name='comments',
        to=Document, verbose_name=_('Document')
    )
    user = models.ForeignKey(
        editable=False, on_delete=models.CASCADE, related_name='comments',
        to=settings.AUTH_USER_MODEL, verbose_name=_('User')
    )
    text = models.TextField(
        verbose_name=_('Text')
    )
    submit_date = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name=_('Date time submitted')
    )

    ###################################### ADD-ON ############################################

    grupo_destino = ArrayField(models.CharField(max_length=100, blank=True), default=list, blank=True)

    ##########################################################################################

    class Meta:
        get_latest_by = 'submit_date'
        ordering = ('-submit_date',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return self.text

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_document_comment_deleted,
        target='document'
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            viewname='comments:comment_details', kwargs={
                'comment_id': self.pk
            }
        )

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_document_comment_created,
            'actor': 'user',
            'action_object': 'document',
            'target': 'self'
        },
        edited={
            'event': event_document_comment_edited,
            'action_object': 'document',
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

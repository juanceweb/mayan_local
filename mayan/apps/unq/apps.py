from django.utils.translation import ugettext_lazy as _
from mayan.apps.common.apps import MayanAppConfig


class UnqApp(MayanAppConfig):
    app_namespace = 'unq'
    app_url = 'unq'
    has_rest_api = True
    has_static_media = False
    has_tests = False
    name = 'mayan.apps.unq'
    verbose_name = _('Unq')

    def ready(self):
        super().ready()

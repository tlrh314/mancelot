from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class CatalogueConfig(AppConfig):
    name = "catalogue"
    verbose_name = _("Catalogue")

    def ready(self):
        pass
        # from catalogue.signals import my_signal
        # post_save.connect(my_signal, sender=self)

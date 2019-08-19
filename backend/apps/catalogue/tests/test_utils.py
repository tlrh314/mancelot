import os
import glob
import logging

from django.conf import settings
from django.test import TestCase

from catalogue.utils import (
    generate_thumbnail,
    optimize_image,
)


class CatalogueUtilsTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.logger = logging.getLogger("console")

    def test_generate_thumbnail(self):
        size = (60, 60)

        for img in glob.glob("{0}/img/test/*".format(settings.STATIC_ROOT)):
            fname, extension = os.path.splitext(img)  # extension contains a leading dot

            generate_thumbnail(self.logger, img, size=size)
            self.assertTrue(
                os.path.exists("{0}_{2}x{3}{1}".format(fname, extension, *size))
            )
            self.assertTrue(
                os.path.isfile("{0}_{2}x{3}{1}".format(fname, extension, *size))
            )

    def test_optimize_image(self):
        for img in glob.glob("{0}/img/test/*".format(settings.STATIC_ROOT)):
            fname, extension = os.path.splitext(img)  # extension contains a leading dot


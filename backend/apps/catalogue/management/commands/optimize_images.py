import os
import glob
import logging

from django.conf import settings

from catalogue.utils import (
    CommandWrapper,
    optimize_image,
)


def optimize_images(logger, cmd_name):
    from PIL import Image
    for img in glob.glob("{0}/img/products/*/*".format(settings.STATIC_ROOT)):
        if not os.path.exists(img) or not os.path.isfile(img):
            logger.warning("WARNING in optimize_images: img '{0}' does not exist!".format(img))

        logger.debug(img)
        optimize_image(logger, img)


class Command(CommandWrapper):
    help = "Generate thumbnails for all product images"

    def handle(self, *args, **options):
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = optimize_images
        self.margs = [ self.cmd_name ]
        self.mkwargs = { }

        logger = logging.getLogger("console")
        super().handle(*args, **options)

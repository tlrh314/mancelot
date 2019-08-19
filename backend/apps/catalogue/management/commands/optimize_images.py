import os
import glob
import logging

from django.conf import settings

from catalogue.utils import (
    CommandWrapper,
    suppress_stdout,
    optimize_image,
)


def optimize_images(logger, cmd_name):
    from PIL import Image
    for img in glob.glob("{0}/img/products/*/*".format(settings.STATIC_ROOT)):
        if not os.path.exists(img) or not os.path.isfile(img):
            logger.warning("WARNING in optimize_images: img '{0}' does not exist!".format(img))

        logger.debug(img)
        optimize_image(logger, img)


def investigate_size_distributions(logger, out):
    import os, glob, numpy
    from matplotlib import pyplot
    pyplot.rcParams.update({ "font.size" : 22 })
    fig, ax = pyplot.subplots(figsize=(12, 9))

    statistics = []
    for size in [64, 128, 256, 512, 1024]:
        images = glob.glob("{0}/img/products/*/*{1}x{1}*".format(settings.STATIC_ROOT, size))
        n = len(images)
        sizes = numpy.zeros(n)
        for i, img in enumerate(images):
            sizes[i] = os.path.getsize(img)  # bytes
        sizes = sizes / 1024.
        sizes = sizes[sizes > 10.]
        statistics.append( (numpy.mean(sizes), numpy.std(sizes)) )
        logger.info("Mean: {0}".format(numpy.mean(sizes)))
        logger.info("Std: {0}".format(numpy.std(sizes)))
        counts, edges = numpy.histogram(sizes, bins=512)
        ax.plot(
            (edges[1:] + edges[:-1]) / 2, counts, drawstyle="steps-mid",
            lw=4, label="{0}x{0}".format(size)
        )

    ax.axvline(10, c="k", ls=":", lw=2)

    ax.set_xlabel("File size [kb]")
    ax.set_ylabel("Count")
    ax.set_xscale("log")
    # ax.set_yscale("log")
    ax.set_ylim(10, ax.get_ylim()[1])
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(out)
    pyplot.close(fig)

    print(statistics)


class Command(CommandWrapper):
    help = "Generate thumbnails for all product images"

    def handle(self, *args, **options):
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = optimize_images
        self.margs = [ self.cmd_name ]
        self.mkwargs = { }

        logger = logging.getLogger("console")
        investigate_size_distributions(logger, "thumbnail_size_distribution_post.png")
        super().handle(*args, **options)
        investigate_size_distributions(self.logger, "thumbnail_size_distribution_pre.png")

import os
import glob

from django.conf import settings

from catalogue.utils import (
    CommandWrapper,
    suppress_stdout,
    generate_thumbnail,
)


def generate_thumbnails(logger, cmd_name):
    from PIL import Image
    for img in glob.glob("{0}/img/products/*/*".format(settings.STATIC_ROOT)):
        if not os.path.exists(img) or not os.path.isfile(img):
            logger.warning("WARNING in generate_thumbnail: img '{0}' does not exist!".format(img))

        if "_64x64" in img: continue
        if "_128x128" in img: continue
        if "_256x256" in img: continue
        if "_512x512" in img: continue
        if "_1024x1024" in img: continue

        logger.debug(img)
        fname, extension = os.path.splitext(img)  # extension contains a leading dot
        if not extension:
            im = Image.open(img)
            extension = "." + str(im.format).lower()
            os.rename(img, img+extension)
            img = img+extension

        for size in [(64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)]:
            out = "{0}_{2}x{3}{1}".format(fname, extension, *size)
            if os.path.exists(out) and os.path.isfile(out):
                continue

            try:
                # with suppress_stdout():
                im = Image.open(img)
                im.thumbnail(size)
                im.save(out)
            except Exception as e:
                logger.info("ERROR generating thumnail\n{0}".format(e))
                continue


def investigate_size_distributions(logger):
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
        sizes = sizes[sizes > 0.]
        statistics.append( (numpy.mean(sizes), numpy.std(sizes)) )
        print("Mean: {0}".format(numpy.mean(sizes)))
        print("Std: {0}".format(numpy.std(sizes)))
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
    fig.savefig("thumbnail_size_distribution.png")
    pyplot.close(fig)

    print(statistics)


class Command(CommandWrapper):
    help = "Generate thumbnails for all product images"

    def handle(self, *args, **options):
        self.cmd_name = __file__.split("/")[-1].replace(".py", "")
        self.method = generate_thumbnails
        self.margs = [ self.cmd_name ]
        self.mkwargs = { }

        super().handle(*args, **options)

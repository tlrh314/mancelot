import os
import json
import logging
import requests

from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from accounts.models import UserModel


def format_time_diff(s, e):
    """ Foramt """
    total_seconds = (e-s).total_seconds()
    n, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(n, 60)
    return "{0:02d}:{1:02d}:{2:02d}".format(int(hours), int(minutes), int(seconds+0.5))


def response_to_json(response):
    return json.loads(response.content.decode("utf8"))


class CommandWrapper(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--is_task",
            dest="is_task", action="store_true", default=False,
            help="The task outputs to console and logfile. When using --is_task, "+\
            "the console output is silenced, thus, we only log to file."
        )

    def handle(self, *args, **options):
        is_task = options["is_task"]

        logdir = "/mancelot/log/commands"
        if not os.path.exists(logdir): os.makedirs(logdir)
        logfilename = "{0}/{1}.txt".format(logdir, self.cmd_name)
        with open(logfilename, "w"):
            # clean up any existing logfile by opening it and writing empty file
            pass

        self.logger = logging.getLogger("console")
        if is_task: self.logger.handlers = []  # do not log to console
        self.logger.addHandler(logging.FileHandler(filename=logfilename))  # always log to file

        start_time = timezone.localtime(timezone.now())
        self.logger.info("manage {0}: started, is_task={1}".format(self.cmd_name, is_task))
        self.logger.info("Start time: {0}\n".format(timezone.localtime(
            start_time).strftime("%d/%m/%Y %H:%M:%S")))

        self.method(self.logger, *self.margs, **self.mkwargs)

        end_time = timezone.now()
        self.logger.info("\n----------")
        self.logger.info("End time: {0}".format(timezone.localtime(
            end_time).strftime("%d/%m/%Y %H:%M:%S")))
        self.logger.info("Execution time: {0}".format(format_time_diff(start_time, end_time)))
        self.logger.info("manage.py {0}: completed.".format(self.cmd_name))


class CeceApiClient(object):
    def __init__(self, *args, **kwargs):
        self.ceceuser, created = UserModel.objects.get_or_create(
            email=settings.CECE_API_USER)
        self.ceceuser.full_name = "CeceUser"; self.ceceuser.save()

    def set_cece_token_headers(self, logger):
        response = requests.post("{0}v1/token/".format(settings.CECE_API_URI), {
                "email": self.ceceuser.email, "password": settings.CECE_API_PASS })
        if response.status_code != 200:
            logger.error("Could not retrieve token in get_cece_api_token")
            sys.exit(1)

        data = response_to_json(response)
        self.headers = {
            "Authorization": "Bearer {0}".format(data["access"]),
            "Accept": "application/json",
            "user-agent": "Mancelot Bot v1.3.3.7"
        }

    def get_list(self, logger, uri, recursive=False, total_count=0):
        logger.debug("GET {0}".format(uri))
        response = requests.get(uri, headers=self.headers)
        if response.status_code != 200:
            logger.error("  Could not retrieve uri = '{0}'. Better stop.".format(uri))
            sys.exit(1)

        results = []

        data = response_to_json(response)
        count = data["count"]
        next = data["next"]
        results += data["results"]
        total_count += len(results)
        logger.debug("  GET {0} retrieved {1}/{2} instances".format(uri, total_count, count))
        logger.debug("    next = {0}".format(next))

        if next and recursive:
            results += self.get_list(logger, next, recursive=True, total_count=total_count)

        return results

    def get_detail(self, logger, uri):
        logger.debug("  GET {0}".format(uri))
        response = requests.get(uri, headers=self.headers)
        if response.status_code != 200:
            logger.error("  Could not retrieve uri = '{0}'. Better stop.".format(uri))
            sys.exit(1)
        return response_to_json(response)

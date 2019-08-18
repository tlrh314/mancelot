import os
import sys
import json
import time
import logging
import requests
from requests.exceptions import ConnectionError, RequestException

from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry

from accounts.models import UserModel


def format_time_diff(s, e):
    """ Foramt """
    total_seconds = (e-s).total_seconds()
    n, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(n, 60)
    return "{0:02d}:{1:02d}:{2:02d}".format(int(hours), int(minutes), int(seconds+0.5))


def response_to_json(response):
    return json.loads(response.content.decode("utf8"))


def download_image(logger, url, save_to, stream=True, attempts=5, sleep=30, w=""):
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    headers = {
        "user-agent": "Mancelot Bot v1.3.3.7",
    }

    logger.info("{0}download_image: {1}".format(w, url))
    for attempt in range(1, attempts+1):
        try:
            response = requests.get(url, stream=stream, headers=headers)
        except (Exception, ConnectionError, RequestException) as e:
            logger.warning("  could not retrieve, now sleep for {0}s".format(
                sleep*attempt))
            time.sleep(sleep*attempt)  # incremental (linear) back-off

        logger.info("{0}  attempt {1}/{2} --> status_code {3}".format(
            w, attempt, attempts, response.status_code
        ))
        if response.status_code == 200: break
        if response.status_code == 404: return False
    else:  # kicks in if no break
        logger.error("{0}ERROR: download_image: {1} failed.".format(w, url))
        return False

    logger.info("{0}SUCCESS, now save_to: {1}".format(w, save_to))
    with open(save_to, "wb") as f:
        for chunk in response:  # reads the data in 128 bytes
            f.write(chunk)
    return True


def call_download_image(logger, url, save_to, instance, field, ctpk, userpk, cmd_name):
    if not os.path.exists(save_to) or not os.path.isfile(save_to):
        if download_image(logger, url, save_to, w="  "):
            # Download success --> update logo
            setattr(instance, field,
                save_to.replace("{0}/".format(settings.STATIC_ROOT), "")
            )
            LogEntry.objects.log_action(
                user_id=userpk,
                content_type_id=ctpk,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=CHANGE,
                change_message="Image for '{0}' downloaded and added by '{1}'".format(
                    field, cmd_name
                )
            )
            instance.save()
        else:  # Download failure
            LogEntry.objects.log_action(
                user_id=userpk,
                content_type_id=ctpk,
                object_id=instance.pk,
                object_repr=str(instance),
                action_flag=CHANGE,
                change_message="Image for '{0}' downloaded failure in '{1}', url = {2}".format(
                    field, cmd_name, url
                )
            )
            return False
    else:  # logo was in Cece format, but we do have the file --> update logo
        setattr(instance, field,
            save_to.replace("{0}/".format(settings.STATIC_ROOT), "")
        )
        LogEntry.objects.log_action(
            user_id=userpk,
            content_type_id=ctpk,
            object_id=instance.pk,
            object_repr=str(instance),
            action_flag=CHANGE,
            change_message="Image for '{0}' updated by '{1}' (from local file)".format(
                field, cmd_name
            )
        )
        instance.save()
    return True


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
        self.ceceuser.full_name = "CeceUser"
        self.ceceuser.save()

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

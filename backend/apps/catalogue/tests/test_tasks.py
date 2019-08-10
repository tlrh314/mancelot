from django.test import TestCase

from catalogue.tasks import retrieve_data_from_cece


class CeceAPITest(TestCase):
    def test_cece_endpoint_is_responsive(self):
        raise NotImplementedError

    def test_get_token(self):
        raise NotImplementedError

    def test_refresh_token(self):
        raise NotImplementedError

    def test_call_command_retrieve_data_from_cece(self):
        raise NotImplementedError

    def test_execute_task_retrieve_data_from_cece(self):
        raise NotImplementedError

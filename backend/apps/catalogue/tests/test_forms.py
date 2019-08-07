from django.test import TestCase


class FixTinyMCEHasTooWideUIFormTest(TestCase):
    def test_fix_tinymc_has_too_wide_ui_form(self):
        # The main thing of interest to test may be whether inheritence is fine
        # in the abstract way we call super, i.e. without (ModelName, self) as args

        # Another test would be a front-end test, i.e. whether the calc call
        # resolves the too wide TinyMCE field
        raise NotImplementedError

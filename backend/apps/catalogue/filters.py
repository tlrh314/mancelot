from django.contrib.admin.filters import (
    AllValuesFieldListFilter,
    ChoicesFieldListFilter,
    RelatedFieldListFilter,
    RelatedOnlyFieldListFilter,
)


# https://github.com/mrts/django-admin-list-filter-dropdown/
class DropdownFilter(AllValuesFieldListFilter):
    template = "catalogue/dropdown_filter.html"


class ChoiceDropdownFilter(ChoicesFieldListFilter):
    template = "catalogue/dropdown_filter.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # By default the title is only the field name, but for a related
        self.title = " ".join(field_path.split("__")).capitalize()


class RelatedDropdownFilter(RelatedFieldListFilter):
    template = "catalogue/dropdown_filter.html"


class RelatedOnlyDropdownFilter(RelatedOnlyFieldListFilter):
    template = "catalogue/dropdown_filter.html"

"""Optionnal shortcuts module for DAL.

This module exports all the public classes for the project. It imports dal
module classes and extension module classes by checking the INSTALLED_APPS
setting:

- if dal_select2 is present, import classes from dal_select2_*,
- with dal_queryset_sequence, import views and fields from it,
- with dal_queryset_sequence and dal_select2, import from
  dal_select2_queryset_sequence,
- with django.contrib.contenttypes, import dal_contenttypes,
- with genericm2m, import dal_genericm2m,
- with gm2m, import dal_gm2m,
- with taggit, import dal_taggit,
- with tagulous, import dal_tagulous.

Note that using this module is optional.
"""

from django.conf import settings as django_settings

from .forms import FutureModelForm

from .views import ViewMixin

from .widgets import (
    Select,
    SelectMultiple,
)


def _installed(*apps):
    for app in apps:
        if app not in django_settings.INSTALLED_APPS:
            return False
    return True

if _installed('dal_select2'):
    from dal_select2.widgets import (
        Select2,
        Select2Multiple,
        ModelSelect2,
        ModelSelect2Multiple,
        TagSelect2,
        ListSelect2
    )
    from dal_select2.views import (
        Select2QuerySetView,
        Select2ListView
    )
    from dal_select2.fields import (
        Select2ListChoiceField,
        Select2ListCreateChoiceField
    )

if _installed('dal_queryset_sequence'):
    from dal_queryset_sequence.fields import (
        QuerySetSequenceModelField,
        QuerySetSequenceModelMultipleField,
    )
    from dal_queryset_sequence.views import (
        BaseQuerySetSequenceView,
    )
    from queryset_sequence import QuerySetSequence

if _installed('dal_select2', 'dal_queryset_sequence'):
    from dal_select2_queryset_sequence.views import (
        Select2QuerySetSequenceView,
    )
    from dal_select2_queryset_sequence.widgets import (
        QuerySetSequenceSelect2,
        QuerySetSequenceSelect2Multiple,
    )

if _installed('dal_select2') and _installed('taggit'):
    from dal_select2_taggit.widgets import TaggitSelect2

if _installed('dal_select2') and _installed('tagging'):
    from dal_select2_tagging.widgets import TaggingSelect2

if _installed('genericm2m') and _installed('dal_queryset_sequence'):
    from dal_genericm2m_queryset_sequence.fields import (
        GenericM2MQuerySetSequenceField
    )

if _installed('gm2m') and _installed('dal_queryset_sequence'):
    from dal_gm2m_queryset_sequence.fields import GM2MQuerySetSequenceField

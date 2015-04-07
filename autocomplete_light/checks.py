import six
from django.core import checks
from django.utils.functional import curry

W001 = checks.Warning(
    "You are trying to use formfield_overrides for a 'widget', "
    "which is not compatible with autocomplete_light's form.",
    id='autocomplete_light.W001',
)


def check_admin_formfield_widget_compatibility(app_configs, **kwargs):
    """Check compatibility with formfield_overrides."""
    errors = []
    from django.contrib.admin import site
    from autocomplete_light.widgets import WidgetBase
    from autocomplete_light.forms import (ModelForm,
                                          get_model_field_form_class)

    we_override = []
    for formf, dbfield in get_model_field_form_class().items():
        we_override += dbfield

    for model, model_admin in six.iteritems(site._registry):
        formfield_overrides = getattr(model_admin, 'formfield_overrides', None)
        form = getattr(model_admin, 'form', None)

        if not formfield_overrides or not issubclass(form, ModelForm):
            continue

        for formfield_override_field, opts in formfield_overrides.items():
            if formfield_override_field in we_override:
                widget = opts.get('widget', None)

                if not widget or issubclass(widget, WidgetBase):
                    continue

                warning = W001
                warning.obj = model
                errors.append(warning)
    return errors
check_admin_formfield_widget_compatibility.tags = ['admin']


def register_default_checks(sender, registry=None, **kwargs):
    """Register default checks for autocomplete_light."""
    checks.register(
        curry(check_admin_formfield_widget_compatibility,
              registry=registry))

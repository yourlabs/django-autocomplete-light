from django import VERSION

if VERSION < (1, 5):
    from django.conf.urls.defaults import patterns, url  # noqa
elif VERSION < (1, 8):
    from django.conf.urls import patterns, url  # noqa
else:
    from django.conf.urls import url  # noqa
    patterns = None


try:
    # Django 1.7 or over use the new application loading system
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

try:
    from django.utils.module_loading import import_string
except ImportError:
    from importlib import import_module
    from django.utils import six
    import sys

    def import_string(dotted_path):
        """
        Import a dotted module path and return the attribute/class designated
        by the last name in the path. Raise ImportError if the import failed.
        Backported from Django 1.8
        """
        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            msg = "%s doesn't look like a module path" % dotted_path
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

        module = import_module(module_path)

        try:
            return getattr(module, class_name)
        except AttributeError:
            msg = 'Module "%s" does not define a "%s" attribute/class' % (
                module_path, class_name)
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])


def urls(urls):
    if patterns:
        return patterns('', *urls)
    return urls

__all__ = (
    'get_model',
    'import_string',
    'urls',
    'url',
    'patterns'
)

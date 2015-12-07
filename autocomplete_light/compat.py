from django import VERSION

if VERSION < (1, 5):
    from django.conf.urls.defaults import patterns, url  # noqa
elif VERSION < (1, 8):
    from django.conf.urls import patterns, url  # noqa
else:
    from django.conf.urls import url  # noqa
    patterns = None


def urls(urls):
    if patterns:
        return patterns('', *urls)
    return urls

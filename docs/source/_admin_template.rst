To enable autocomplete form widgets, you need to load:

- jQuery
- autocomplete_light/autocomplete.js
- autocomplete_light/widget.js

Optionally:

- autocomplete_light/style.css
- autocomplete_light/remote.js

A quick way to enable all this in the admin is to use the following
``admin/base_site.html`` template::

    {% extends "admin/base.html" %}
    {% load static %}

    {% block extrahead %}
        {{ block.super }}
        <script src="{% static 'admin/js/vendor/jquery/jquery.min.js' %}" type="text/javascript"></script>
        {% include 'autocomplete_light/static.html' %}
    {% endblock %}

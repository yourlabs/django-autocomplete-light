To enable autocomplete form widgets, you need to load:

- jQuery
- autocomplete_light/autocomplete.js
- autocomplete_light/widget.js

Optionally:

- autocomplete_light/style.css
- autocomplete_light/remote.js

A quick way to enable all this in the admin, is to replace template
``admin/base_site.html``, ie.::

    {% extends "admin/base.html" %}

    {% block extrahead %}
        <script src="{{ STATIC_URL }}jquery.js" type="text/javascript"></script>
        {% include 'autocomplete_light/static.html' %}
    {% endblock %}

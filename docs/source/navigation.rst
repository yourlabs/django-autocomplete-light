.. _navigation:

Making a global navigation autocomplete
=======================================

This guide demonstrates how to make a global navigation autocomplete
like on Facebook.

Note that there are many ways to implement such a feature, we're just
describing a simple one.

A simple view
-------------

As we're just going to use :ref:`autocomplete.js` for this, we only need a view
to render the autocomplete. For example:

.. code-block:: python

    from django import shortcuts
    from django.db.models import Q
    
    from autocomplete_light.example_apps.music.models import Artist, Genre

    def navigation_autocomplete(request,
        template_name='navigation_autocomplete/autocomplete.html'):

        q = request.GET.get('q', '')

        queries = {}
        
        queries['artists'] = Artist.objects.filter(
            Q(name__icontains=q) |
            Q(genre__name__icontains=q)
        ).distinct()[:6]

        queries['genres'] = Genre.objects.filter(name__icontains=q)[:6]

        return shortcuts.render(request, template_name, queries)

Along with a trivial template for ``navigation_autocomplete/autocomplete.html``
would work:

.. code-block:: django

    <span class="separator">Artists</span>
    {% for artist in artists %}
    <a class="block choice" href="{{ artist.get_absolute_url }">{{ artist }}</a>
    {% endfor %}

    <span class="separator">Genres</span>
    {% for genre in genre %}
    <a class="block choice" href="{{ genre.get_absolute_url }}">{{ genre }}</a>
    {% endfor %}    

A basic autocomplete configuration
----------------------------------

That's a pretty basic usage of :ref:`autocomplete.js`, concepts are
detailed in :ref:`navigation-autocomplete-example`, this is what it
looks like:

.. code-block:: javascript

    // Change #yourInput by a selector that matches the input you want to use
    // for the navigation autocomplete.
    $('#yourInput').yourlabsAutocomplete({
        // Url of the view you just created
        url: '{% url "your_autocomplete_url" %}',

        // With keyboard, we should iterate around <a> tags in the autocomplete
        choiceSelector: 'a',
    }).input.bind('selectChoice', function(e, choice, autocomplete) {
        // When a choice is selected, open it. Note: this is not needed for
        // mouse click on the links of course, but this is necessary for keyboard
        // selection.
        window.location.href = choice.attr('href');
    });

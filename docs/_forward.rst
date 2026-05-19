Filtering results based on other form fields (forwarding)
=========================================================

- Example source: `test_project/alight_linked_data
  <https://github.com/yourlabs/django-autocomplete-light/tree/alight-backend/test_project/alight_linked_data>`_
- Live demo: `Admin / Alight Linked Data / Add
  <http://localhost:8000/admin/alight_linked_data/tmodel/add/>`_

The ``forward`` widget argument works the same way as in any DAL backend:

.. code-block:: python

    class PersonForm(forms.ModelForm):
        continent = forms.ChoiceField(choices=CONTINENT_CHOICES)

        class Meta:
            model = Person
            fields = ('__all__',)
            widgets = {
                'birth_country': autocomplete.ModelAlight(
                    url='country-autocomplete',
                    forward=['continent'],
                )
            }

In the view, read the forwarded value from ``self.forwarded``:

.. code-block:: python

    class CountryAutocomplete(autocomplete.AlightQuerySetView):
        def get_queryset(self):
            qs = Country.objects.all()
            continent = self.forwarded.get('continent', None)
            if continent:
                qs = qs.filter(continent=continent)
            if self.q:
                qs = qs.filter(name__istartswith=self.q)
            return qs

All forwarding features (``forward.Field``,
``forward.Const``, ``forward.Self``, ``forward.JavaScript``, renaming) work
the same — they live in :py:mod:`dal.forward` and are backend-independent.

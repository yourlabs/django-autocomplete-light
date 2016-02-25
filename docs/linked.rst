Filtering results based on the value of other fields in the form
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say we want to add a "Continent" choice field in the form, and filter the
countries based on the value on this field. We then need the widget to pass the
value of the continent field to the view when it fetches data. We can use the
``forward`` widget argument to do this:

.. code-block:: python

    class PersonForm(forms.ModelForm):
        continent = forms.ChoiceField(choices=CONTINENT_CHOICES)

        class Meta:
            model = Person
            fields = ('__all__')
            widgets = {
                'birth_country': autocomplete.ModelSelect2(url='country-autocomplete'
                                                           forward=['continent'])
            }

This will pass the value for the "continent" form field in the AJAX request,
and we can then filter as such in the view:

.. code-block:: python

    class CountryAutocomplete(autocomplete.Select2QuerySetView):
        def get_queryset(self):
            if not self.request.is_authenticated():
                return Country.objects.none()

            qs = Country.objects.all()

            continent = self.forwarded.get('continent', None)

            if continent:
                qs = qs.filter(continent=continent)

            if self.q:
                qs = qs.filter(name__istartswith=self.q)

            return qs

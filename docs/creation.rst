Creation of new choices in the autocomplete form
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Auto-creation of one-to-one and one-to-many (foreign-key) relations
===================================================================

By default, Django's ModelChoiceField is used for validation and it only allows
to choose existing choices. To enable creating choices during validation, we
can use the CreateModelField`` form field, ie:

.. code-block:: python

    class YourCountryCreateField(autocomplete.CreateModelField):
        def create_value(self, value):
            return Country.objects.create(name=value).pk


    class PersonForm(forms.ModelForm):
        birth_country = YourCountryCreateField(
            required=False,  # leave out if your model field doesn't have blank=True
            queryset=Country.objects.all(),
            widget=autocomplete.ModelSelect2(url='country-autocomplete')
        )

        class Meta:
            model = Person
            fields = ('__all__')

Auto-creation of many-to-many relations
=======================================

Note that for we could do the same for a multiple relation, using
autocomplete.CreateModelMultipleField and autocomplete.ModelSelect2Multiple, ie.:

.. code-block:: python

    class YourCountryCreateMultipleField(autocomplete.CreateModelMultipleField):
        def create_value(self, value):
            return Country.objects.create(name=value).pk


    class PersonForm(forms.ModelForm):
        visited_countries = YourCountryCreateMultipleField(
            required=False,  # leave out if your model field doesn't have blank=True
            queryset=Country.objects.all(),
            widget=autocomplete.ModelSelect2Multiple(url='country-autocomplete')
        )

        class Meta:
            model = Person
            fields = ('__all__')

Deduplicating creation code with mixins
=======================================

Of course, we could use a mixin to avoid duplicating code if we wanted both,
ie.:

.. code-block:: python

    class CountryCreateFieldMixin(object):
        def create_value(self, value):
            return Country.objects.create(name=value).pk


    class CountryCreateField(CountryCreateFieldMixin,
                             autocomplete.CreateModelField):
        pass


    class CountryCreateMultipleField(CountryCreateFieldMixin,
                                     autocomplete.CreateModelMultipleField):
        pass

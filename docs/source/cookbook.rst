Voodoo black magic
------------------

Various cooking recipes ``your_app/autocomplete_light_registry.py``::

    # Extra **kwargs are used as class properties in the subclass.
    autocomplete_light.register(SomeModel,
        name='AutocompleNewSomeModel',
        choices=SomeModel.objects.filter(new=True))

    # It is possible to override javascript options from Python.
    autocomplete_light.register(OtherModel, 
        autocomplete_js_attributes={
            'minimum_character': 0, 
            'placeholder': 'Other model name ?',
        }
    )

    # But you can make your subclass yourself and override methods.
    class AutocompleteYourModel(autocomplete_light.AutocompleteTemplateModel):
        template_name = 'your_app/your_special_choice_template.html'

        autocomplete_js_attributes = {
            'minimum_character': 4, 
        }

        widget_js_attributes = {
            'max_values': 6,
        }

        def choices_for_request(self):
            return super(AutocompleteYourModel, self).choices_for_request(
                ).exclude(extra=self.request.GET['extra'])

    # Just pass the class to register as well.
    autocomplete_light.register(YourModel, YourModelAutocomplete)

    # This will subclass the subclass, using extra kwargs as class attributes.
    autocomplete_light.register(YourModel, YourModelAutocomplete, 
        name='YourModelOtherAutocomplete', 
        choice_template='your_app/other_template.html')

Various cooking recipes far ``your_app/forms.py``::

    # Use as much registered autocompletes as possible.
    SomeModelForm = autocomplete_light.modelform_factory(SomeModel, 
        exclude=('some_field')

    # Same with a custom modelform, using Meta.get_widgets_dict().
    class CustomModelForm(forms.ModelForm):
        some_extra_field = forms.CharField()

        class Meta:
            model = SomeModel
            widgets = autocmoplete_light.get_widgets_dict(SomeModel)

    # Using widgets directly in any kind of form.
    class NonModelForm(forms.Form):
        user = forms.ModelChoiceField(User.objects.all(),
            widget=autocomplete_light.ChoiceWidget('UserAutocomplete'))

        cities = forms.ModelMultipleChoiceField(City.objects.all(),
            widget=autocomplete_light.MultipleChoiceWidget('CityAutocomplete',
                # Those attributes have priority over the Autocomplete ones.
                autocomplete_js_attributes={'minimum_characters': 0,
                                            'placeholder': 'Choose 3 cities ...'},
                widget_js_attributes={'max_values': 3}))

        tags = autocomplete_light.TextWidget('TagAutocomplete')


Django 1.3 support workarounds
==============================

The app is was developed for Django 1.4. However, there are workarounds to get
it to work with Django 1.3 too. This document attemps to provide an exhaustive
list of notes that should be taken in account when using the app with
django-autocomplete-light.

modelform_factory
-----------------

The provided autocomplete_light.modelform_factory relies on Django 1.4's
modelform_factory that accepts a 'widgets' dict.

Django 1.3 does not allow such an argument. You may however define your form as
such::

    class AuthorForm(forms.ModelForm):
        class Meta:
            model = Author
            widgets = autocomplete_light.get_widgets_dict(Author)

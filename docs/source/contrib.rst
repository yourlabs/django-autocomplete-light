Support for django-generic-m2m
------------------------------

See :doc:`GenericManyToMany documentation<generic>`.

Support for django-hvad
-----------------------

.. automodule:: autocomplete_light.contrib.hvad
   :members:

Support for django-taggit
-------------------------

`django-taggit
<https://github.com/alex/django-taggit>`_ does it slightly differently. It is
supported by autocomplete_light as of 1.0.25. First you need to register the taggit Tag class and for each form you need to set the TaggitWidget.

First register the tag::

   from taggit.models import Tag
   import autocomplete_light.shortcuts as al
   al.register(Tag)

Every form which should have the autocomplete taggit widget should look like::
    
   from autocomplete_light.contrib.taggit_field import TaggitField, TaggitWidget
        
   class AppEditForm(forms.ModelForm):
      tags = TaggitField(widget=TaggitWidget('TagAutocomplete'))
      class Meta:
         model = App

.. automodule:: autocomplete_light.contrib.taggit_tagfield
   :members:

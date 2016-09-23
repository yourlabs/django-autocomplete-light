django-autocomplete-light FAQ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Table of contents
========



- TypeError: ModelChoiceField is taking integer rather than Model as arguments 


.. _queryset-view:

TypeError
===========================


Exception Type: TypeError
Exception Value: int() argument must be a string, a bytes-like object or a number, not 'Your_Model'

Traceback:

.. code-block:: python

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\core\handlers\exception.py" in inner
      39.             response = get_response(request)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\core\handlers\base.py" in _get_response
      187.                 response = self.process_exception_by_middleware(e, request)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\core\handlers\base.py" in _get_response
      185.                 response = wrapped_callback(request, *callback_args, **callback_kwargs)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\contrib\auth\decorators.py" in _wrapped_view
      23.                 return view_func(request, *args, **kwargs)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\contrib\auth\decorators.py" in _wrapped_view
      23.                 return view_func(request, *args, **kwargs)

    File "C:\Users\hansong.li\Documents\GitHub\equipCal\calbase\views.py" in post_update
      129.     return render(request, 'calbase/default_edit.html', context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\shortcuts.py" in render
      30.     content = loader.render_to_string(template_name, context, request, using=using)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\loader.py" in render_to_string
      68.     return template.render(context, request)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\backends\django.py" in render
      66.             return self.template.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render
      208.                     return self._render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in _render
      199.         return self.nodelist.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render
      994.                 bit = node.render_annotated(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render_annotated
      961.             return self.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\loader_tags.py" in render
      174.         return compiled_parent._render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in _render
      199.         return self.nodelist.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render
      994.                 bit = node.render_annotated(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render_annotated
      961.             return self.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\loader_tags.py" in render
      70.                 result = block.nodelist.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render
      994.                 bit = node.render_annotated(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render_annotated
      961.             return self.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\templatetags\crispy_forms_tags.py" in render
      214.         c = self.get_render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\templatetags\crispy_forms_tags.py" in get_render
      133.                 actual_form.form_html = helper.render_layout(actual_form, node_context, template_pack=self.template_pack)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\helper.py" in render_layout
      297.             template_pack=template_pack

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\layout.py" in render
      138.         return self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\layout.py" in get_rendered_fields
      102.             for field in self.fields

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\layout.py" in <genexpr>
      102.             for field in self.fields

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\utils.py" in render_field
      73.                 form, form_style, context, template_pack=template_pack,

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\layout.py" in render
      358.         fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\layout.py" in get_rendered_fields
      102.             for field in self.fields

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\layout.py" in <genexpr>
      102.             for field in self.fields

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\utils.py" in render_field
      73.                 form, form_style, context, template_pack=template_pack,

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\layout.py" in render
      358.         fields = self.get_rendered_fields(form, form_style, context, template_pack, **kwargs)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\layout.py" in get_rendered_fields
      102.             for field in self.fields

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\layout.py" in <genexpr>
      102.             for field in self.fields

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\crispy_forms\utils.py" in render_field
      162.             html = template.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\backends\django.py" in render
      66.             return self.template.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render
      208.                     return self._render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in _render
      199.         return self.nodelist.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render
      994.                 bit = node.render_annotated(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render_annotated
      961.             return self.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\defaulttags.py" in render
      323.                 return nodelist.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render
      994.                 bit = node.render_annotated(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render_annotated
      961.             return self.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\defaulttags.py" in render
      323.                 return nodelist.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render
      994.                 bit = node.render_annotated(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render_annotated
      961.             return self.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\defaulttags.py" in render
      323.                 return nodelist.render(context)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\template\base.py" in render
      997.             bits.append(force_text(bit))

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\utils\encoding.py" in force_text
      76.                     s = six.text_type(s)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\utils\html.py" in <lambda>
      391.         klass.__str__ = lambda self: mark_safe(klass_str(self))

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\forms\boundfield.py" in __str__
      43.         return self.as_widget()

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\forms\boundfield.py" in as_widget
      101.         return force_text(widget.render(name, self.value(), attrs=attrs))

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\forms\widgets.py" in render
      600.         options = self.render_options(value)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\dal\widgets.py" in render_options
      75.             self.filter_choices_to_render(selected_choices)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\dal\widgets.py" in filter_choices_to_render
      113.             pk__in=[c for c in selected_choices if c]

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\db\models\query.py" in filter
      794.         return self._filter_or_exclude(False, *args, **kwargs)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\db\models\query.py" in _filter_or_exclude
      812.             clone.query.add_q(Q(*args, **kwargs))

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\db\models\sql\query.py" in add_q
      1227.         clause, _ = self._add_q(q_object, self.used_aliases)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\db\models\sql\query.py" in _add_q
      1253.                     allow_joins=allow_joins, split_subq=split_subq,

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\db\models\sql\query.py" in build_filter
      1187.             condition = self.build_lookup(lookups, col, value)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\db\models\sql\query.py" in build_lookup
      1083.                 return final_lookup(lhs, rhs)

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\db\models\lookups.py" in __init__
      19.         self.rhs = self.get_prep_lookup()

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\db\models\lookups.py" in get_prep_lookup
      261.             return [self.lhs.output_field.get_prep_value(v) for v in self.rhs]

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\db\models\lookups.py" in <listcomp>
      261.             return [self.lhs.output_field.get_prep_value(v) for v in self.rhs]

    File "C:\Users\hansong.li\AppData\Local\Programs\Python\Python35-32\lib\site-packages\django\db\models\fields\__init__.py" in get_prep_value
      946.         return int(value)

    Exception Type: TypeError at /calbase/equipment/1/update/
    Exception Value: int() argument must be a string, a bytes-like object or a number, not 'Tests'

.. 



solution:: This error may be caused by problem in javascript location. In the old documentation, it asks you to put:

.. code-block:: python

    <script type="text/javascript" src="/static/collected/admin/js/vendor/jquery/jquery.js"></script>

    {{ form.media }}
..

inside the template that you would like to render autocomplete field. Using this instead:

.. code-block:: python

    <script type="text/javascript" src="{% static 'admin/js/vendor/jquery/jquery.js' %}"></script>

    {{ form.media }}
..


may solve the problem. 

Also, check in your modelform if the field you used agrees with widget. If it is Foreign Key field, make it:

.. code-block:: python

    foreign_key_field = forms.ModelChoiceField(
        queryset=YourForeignKeyModel.objects.all(),
        widget=autocomplete.ModelSelect2(url='your_url_name')
    )
..


If it is a many-to-many field, make it:

.. code-block:: python

    foreign_key_field = forms.ModelMultipleChoiceField(
        queryset=YourForeignKeyModel.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='your_url_name')
    )
..



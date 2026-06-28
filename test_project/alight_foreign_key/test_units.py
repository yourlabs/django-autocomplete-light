"""Unit tests for dal_alight views, widgets, and fields."""


from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from dal_alight.fields import AlightListChoiceField, AlightListCreateChoiceField
from dal_alight.views import (
    AlightGroupListView,
    AlightGroupQuerySetView,
    AlightListView,
    AlightQuerySetView,
)
from dal_alight.widgets import (
    Alight,
    AlightMultiple,
    ListAlight,
    ModelAlight,
    ModelAlightMultiple,
    TagAlight,
    TaggitAlight,
)

User = get_user_model()


# ---------------------------------------------------------------------------
# Helper: minimal model for widget tests
# ---------------------------------------------------------------------------

def get_tmodel():
    from django.apps import apps
    return apps.get_model('alight_foreign_key', 'TModel')


# ---------------------------------------------------------------------------
# View tests
# ---------------------------------------------------------------------------

class AlightQuerySetViewGetTest(TestCase):
    """AlightQuerySetView GET returns correct HTML fragments."""

    def setUp(self):
        self.TModel = get_tmodel()
        self.factory = RequestFactory()
        self.a = self.TModel.objects.create(name='apple')
        self.b = self.TModel.objects.create(name='banana')
        self.c = self.TModel.objects.create(name='cherry')

    def _get(self, q='', **kwargs):
        view = AlightQuerySetView.as_view(model=self.TModel, **kwargs)
        request = self.factory.get('/', {'q': q})
        request.user = User()
        return view(request)

    def test_returns_html_content_type(self):
        r = self._get()
        self.assertEqual(r['Content-Type'], 'text/html; charset=utf-8')

    def test_empty_query_returns_all(self):
        r = self._get()
        content = r.content.decode()
        self.assertIn('apple', content)
        self.assertIn('banana', content)
        self.assertIn('cherry', content)

    def test_query_filters_results(self):
        r = self._get(q='app')
        content = r.content.decode()
        self.assertIn('apple', content)
        self.assertNotIn('banana', content)

    def test_result_has_data_value_attribute(self):
        r = self._get(q='apple')
        content = r.content.decode()
        self.assertIn('data-value="%s"' % self.a.pk, content)

    def test_no_create_option_without_create_field(self):
        r = self._get(q='newitem')
        self.assertNotIn('data-create', r.content.decode())

    def test_create_option_shown_when_no_match(self):
        superuser = User.objects.create_superuser('su', password='pw')
        view = AlightQuerySetView.as_view(
            model=self.TModel, create_field='name',
        )
        request = self.factory.get('/', {'q': 'unique_xyz'})
        request.user = superuser
        r = view(request)
        content = r.content.decode()
        self.assertIn('data-create', content)
        self.assertIn('unique_xyz', content)

    def test_create_option_hidden_when_exact_match(self):
        superuser = User.objects.create_superuser('su2', password='pw')
        view = AlightQuerySetView.as_view(
            model=self.TModel, create_field='name',
        )
        request = self.factory.get('/', {'q': 'apple'})
        request.user = superuser
        r = view(request)
        self.assertNotIn('data-create', r.content.decode())

    def test_create_option_case_insensitive(self):
        superuser = User.objects.create_superuser('su3', password='pw')
        view = AlightQuerySetView.as_view(
            model=self.TModel, create_field='name',
        )
        request = self.factory.get('/', {'q': 'Apple'})
        request.user = superuser
        r = view(request)
        self.assertNotIn('data-create', r.content.decode())

    def test_create_option_requires_add_permission(self):
        regular = User.objects.create_user('regular', password='pw')
        view = AlightQuerySetView.as_view(
            model=self.TModel, create_field='name',
        )
        request = self.factory.get('/', {'q': 'newitem'})
        request.user = regular
        r = view(request)
        self.assertNotIn('data-create', r.content.decode())

    def test_pagination_sentinel_included(self):
        # Create enough objects to trigger pagination (paginate_by=10).
        for i in range(15):
            self.TModel.objects.create(name='pg_%s' % i)
        r = self._get(q='pg_')
        self.assertIn('data-next-page', r.content.decode())

    def test_invalid_forward_returns_400(self):
        request = self.factory.get('/', {'forward': '{bad json'})
        request.user = User()
        view = AlightQuerySetView.as_view(model=self.TModel)
        r = view(request)
        self.assertEqual(r.status_code, 400)

    def test_post_creates_object(self):
        superuser = User.objects.create_superuser('su_post', password='pw')
        view = AlightQuerySetView.as_view(
            model=self.TModel, create_field='name',
        )
        request = self.factory.post('/', {'text': 'brand_new'})
        request.user = superuser
        r = view(request)
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn('data-value=', body)
        self.assertIn('brand_new', body)
        self.assertTrue(self.TModel.objects.filter(name='brand_new').exists())

    def test_post_without_permission_returns_403(self):
        regular = User.objects.create_user('reg_post', password='pw')
        view = AlightQuerySetView.as_view(
            model=self.TModel, create_field='name',
        )
        request = self.factory.post('/', {'text': 'nope'})
        request.user = regular
        r = view(request)
        self.assertEqual(r.status_code, 403)

    def test_invalid_method_returns_405(self):
        request = self.factory.put('/')
        request.user = User()
        view = AlightQuerySetView.as_view(model=self.TModel)
        r = view(request)
        self.assertEqual(r.status_code, 405)


class AlightListViewTest(TestCase):
    """AlightListView GET/POST behaviour."""

    class FruitView(AlightListView):
        fruits = ['apple', 'apricot', 'banana', 'cherry']

        def get_list(self):
            return self.fruits

    class FruitViewWithCreate(FruitView):
        def create(self, text):
            self.fruits.append(text)
            return text

    class TupleListView(AlightListView):
        def get_list(self):
            return [('a', 'Alpha'), ('b', 'Beta'), ('c', 'Gamma')]

    def _get(self, view_cls, q='', **kwargs):
        factory = RequestFactory()
        request = factory.get('/', {'q': q})
        request.user = User()
        view = view_cls.as_view()
        return view(request)

    def _post(self, view_cls, text):
        factory = RequestFactory()
        request = factory.post('/', {'text': text})
        request.user = User()
        return view_cls.as_view()(request)

    def test_returns_all_without_query(self):
        r = self._get(self.FruitView)
        content = r.content.decode()
        self.assertIn('apple', content)
        self.assertIn('banana', content)

    def test_filters_by_query(self):
        r = self._get(self.FruitView, q='ap')
        content = r.content.decode()
        self.assertIn('apple', content)
        self.assertIn('apricot', content)
        self.assertNotIn('banana', content)

    def test_result_has_data_value(self):
        r = self._get(self.FruitView, q='apple')
        self.assertIn('data-value="apple"', r.content.decode())

    def test_create_option_shown_when_create_defined(self):
        r = self._get(self.FruitViewWithCreate, q='dragonfruit')
        self.assertIn('data-create', r.content.decode())
        self.assertIn('dragonfruit', r.content.decode())

    def test_no_create_option_without_create_method(self):
        r = self._get(self.FruitView, q='anything')
        self.assertNotIn('data-create', r.content.decode())

    def test_post_creates_and_returns_html(self):
        r = self._post(self.FruitViewWithCreate, 'dragonfruit')
        self.assertEqual(r.status_code, 200)
        content = r.content.decode()
        self.assertIn('data-value="dragonfruit"', content)
        self.assertIn('dragonfruit', content)

    def test_post_without_create_returns_405(self):
        factory = RequestFactory()
        request = factory.post('/', {'text': 'x'})
        request.user = User()
        response = self.FruitView.as_view()(request)
        self.assertEqual(response.status_code, 405)

    def test_tuple_list_value_label(self):
        r = self._get(self.TupleListView, q='ph')
        content = r.content.decode()
        self.assertIn('data-value="a"', content)
        self.assertIn('Alpha', content)
        self.assertNotIn('Beta', content)

    def test_content_type_is_html(self):
        r = self._get(self.FruitView)
        self.assertEqual(r['Content-Type'], 'text/html; charset=utf-8')


# ---------------------------------------------------------------------------
# Widget render tests
# ---------------------------------------------------------------------------

class AlightWidgetMixinMediaTest(TestCase):
    def test_media_includes_autocomplete_js(self):
        w = ModelAlight(url='x')
        media_js = str(w.media)
        self.assertIn('autocomplete-light.js', media_js)

    def test_media_includes_dal_django_js(self):
        w = ModelAlight(url='x')
        media_js = str(w.media)
        self.assertIn('dal-django.js', media_js)

    def test_media_includes_css(self):
        w = ModelAlight(url='x')
        media_css = str(w.media)
        self.assertIn('autocomplete-light.css', media_css)

    def test_media_uses_module_scripts_on_django_6(self):
        import django

        w = ModelAlight(url='x')
        media_js = str(w.media)
        if django.VERSION >= (6, 0):
            self.assertIn('type="module"', media_js)
        else:
            self.assertNotIn('type="module"', media_js)


class ModelAlightRenderTest(TestCase):
    def setUp(self):
        self.TModel = get_tmodel()

    def _widget(self, **kw):
        from django.forms import ModelChoiceField
        field = ModelChoiceField(queryset=self.TModel.objects.all())
        w = ModelAlight(url='alight_fk')
        w.choices = field.widget.choices
        w.choices.field = field
        return w

    def test_renders_autocomplete_select_wrapper(self):
        w = self._widget()
        html = w.render('test', None)
        self.assertIn('<autocomplete-select', html)
        self.assertIn('</autocomplete-select>', html)

    def test_renders_id_on_search_input(self):
        w = self._widget()
        html = w.render('test', None, attrs={'id': 'id_test'})
        self.assertIn('id="id_test"', html)
        self.assertNotIn('<autocomplete-select id=', html)

    def test_renders_hidden_values_slot(self):
        w = self._widget()
        html = w.render('test', None)
        self.assertNotIn('slot="select"', html)
        self.assertNotIn('<select', html)

    def test_renders_deck_span(self):
        w = self._widget()
        html = w.render('test', None)
        self.assertIn('<span slot="deck">', html)

    def test_renders_autocomplete_select_input(self):
        w = self._widget()
        html = w.render('test', None)
        self.assertIn('<autocomplete-select-input', html)
        self.assertIn('url="', html)

    def test_renders_without_url_when_url_is_none(self):
        from django.forms import ModelChoiceField
        field = ModelChoiceField(queryset=self.TModel.objects.all())
        w = ModelAlight(url=None)
        w.choices = field.widget.choices
        w.choices.field = field
        # Should not crash
        html = w.render('test', None)
        self.assertIn('<autocomplete-select-input', html)

    def test_allow_multiple_selected_false(self):
        w = ModelAlight(url='alight_fk')
        self.assertFalse(w.allow_multiple_selected)

    def test_model_alight_multiple_allow_multiple(self):
        w = ModelAlightMultiple(url='alight_fk')
        self.assertTrue(w.allow_multiple_selected)

    def test_forward_conf_rendered_when_forward_set(self):
        from django.forms import ModelChoiceField
        field = ModelChoiceField(queryset=self.TModel.objects.all())
        w = ModelAlight(url='alight_fk', forward=['name'])
        w.choices = field.widget.choices
        w.choices.field = field
        html = w.render('test', None, attrs={'id': 'id_test'})
        self.assertIn('dal-forward-conf', html)

    def test_no_forward_conf_without_forward(self):
        from django.forms import ModelChoiceField
        field = ModelChoiceField(queryset=self.TModel.objects.all())
        w = ModelAlight(url='alight_fk')
        w.choices = field.widget.choices
        w.choices.field = field
        html = w.render('test', None)
        self.assertNotIn('dal-forward-conf', html)


class AlightInitialRenderMixinTest(TestCase):
    def setUp(self):
        self.TModel = get_tmodel()
        self.obj = self.TModel.objects.create(name='pre-filled')

    def _widget(self, value):
        from django.forms import ModelChoiceField
        # Use full queryset — the mixin filters it down to the selected pk.
        field = ModelChoiceField(queryset=self.TModel.objects.all())
        w = ModelAlight(url='alight_fk')
        w.choices = field.widget.choices
        w.choices.field = field
        return w.render('test', value, attrs={'id': 'id_test'})

    def test_prefills_single_value(self):
        html = self._widget(self.obj.pk)
        self.assertIn('pre-filled', html)
        self.assertIn('slot="values"', html)
        self.assertIn('type="hidden"', html)

    def test_does_not_fail_on_none_value(self):
        html = self._widget(None)
        self.assertIsInstance(html, str)

    def _widget_multiple(self, values):
        from django.forms import ModelMultipleChoiceField
        field = ModelMultipleChoiceField(queryset=self.TModel.objects.all())
        w = ModelAlightMultiple(url='alight_fk')
        w.choices = field.widget.choices
        w.choices.field = field
        return w.render('test', values, attrs={'id': 'id_test'})

    def test_prefills_multiple_values(self):
        obj2 = self.TModel.objects.create(name='second')
        html = self._widget_multiple([self.obj.pk, obj2.pk])
        self.assertIn('pre-filled', html)
        self.assertIn('second', html)


class NonQuerysetWidgetTest(TestCase):
    """Alight, AlightMultiple, ListAlight render correctly."""

    CHOICES = [('a', 'Alpha'), ('b', 'Beta')]

    def test_alight_renders_component(self):
        # Use a path (contains '/') so WidgetMixin doesn't try to reverse it.
        w = Alight(url='/autocomplete/', choices=self.CHOICES)
        html = w.render('field', None, attrs={'id': 'id_field'})
        self.assertIn('id="id_field"', html)

    def test_alight_without_url_raises(self):
        with self.assertRaises(ValueError):
            Alight(url=None, choices=self.CHOICES)

    def test_alight_multiple_allow_multiple(self):
        w = AlightMultiple(url='/autocomplete/', choices=self.CHOICES)
        self.assertTrue(w.allow_multiple_selected)

    def test_list_alight_renders_component(self):
        w = ListAlight(url='/list-autocomplete/', choices=self.CHOICES)
        html = w.render('field', None, attrs={'id': 'id_field'})
        self.assertIn('url="', html)


class TagAlightTest(TestCase):
    """TagAlight value handling."""

    def _widget(self):
        # Use a path so WidgetMixin doesn't try to reverse a URL name.
        w = TagAlight(url='/tag-autocomplete/')
        return w

    def test_value_from_datadict_joins_with_comma(self):
        w = self._widget()
        data = {'tags': ['foo', 'bar', 'baz']}
        result = w.value_from_datadict(data, {}, 'tags')
        self.assertEqual(result, 'foo,bar,baz')

    def test_format_value_splits_comma_string(self):
        w = self._widget()
        result = w.format_value('foo,bar')
        self.assertEqual(result, {'foo', 'bar'})

    def test_format_value_handles_list(self):
        w = self._widget()
        result = w.format_value(['foo', 'bar'])
        self.assertEqual(result, {'foo', 'bar'})

    def test_optgroups_creates_selected_options(self):
        w = self._widget()
        groups = w.optgroups('tags', 'foo,bar')
        options = groups[0][1]
        values = [o['value'] for o in options]
        self.assertIn('foo', values)
        self.assertIn('bar', values)
        for o in options:
            self.assertTrue(o['selected'])

    def test_render_includes_component(self):
        w = self._widget()
        html = w.render('tags', 'foo,bar', attrs={'id': 'id_tags'})
        self.assertIn('id="id_tags"', html)

    def test_allow_multiple_selected(self):
        self.assertTrue(self._widget().allow_multiple_selected)


# ---------------------------------------------------------------------------
# Field tests
# ---------------------------------------------------------------------------

class AlightListChoiceFieldTest(TestCase):
    CHOICES = ['apple', 'banana', 'cherry']

    def test_accepts_valid_choice(self):
        field = AlightListChoiceField(choice_list=self.CHOICES)
        self.assertEqual(field.clean('apple'), 'apple')

    def test_rejects_invalid_choice(self):
        from django.core.exceptions import ValidationError
        field = AlightListChoiceField(choice_list=self.CHOICES)
        with self.assertRaises(ValidationError):
            field.clean('dragonfruit')

    def test_callable_choices(self):
        field = AlightListChoiceField(choice_list=lambda: self.CHOICES)
        self.assertEqual(field.clean('banana'), 'banana')

    def test_tuple_choices(self):
        choices = [('a', 'Alpha'), ('b', 'Beta')]
        field = AlightListChoiceField(choice_list=choices)
        self.assertEqual(field.clean('a'), 'a')


class AlightListCreateChoiceFieldTest(TestCase):
    CHOICES = ['apple', 'banana']

    def test_accepts_valid_choice(self):
        field = AlightListCreateChoiceField(choice_list=self.CHOICES)
        self.assertEqual(field.clean('apple'), 'apple')

    def test_accepts_arbitrary_value(self):
        field = AlightListCreateChoiceField(choice_list=self.CHOICES)
        # Should not raise even though 'dragonfruit' is not in CHOICES.
        result = field.clean('dragonfruit')
        self.assertEqual(result, 'dragonfruit')

    def test_rejects_empty_when_required(self):
        from django.core.exceptions import ValidationError
        field = AlightListCreateChoiceField(choice_list=self.CHOICES, required=True)
        with self.assertRaises(ValidationError):
            field.clean('')


# ---------------------------------------------------------------------------
# Forward cloning (regression guard)
# ---------------------------------------------------------------------------

class ForwardCloningTest(TestCase):
    def test_forwards_are_cloned_on_deepcopy(self):
        import copy
        w = ModelAlight(url='x', forward=['a', 'b'])
        w2 = copy.deepcopy(w)
        w2.forward.append('c')
        self.assertNotIn('c', w.forward)


# ---------------------------------------------------------------------------
# AlightGroupQuerySetView
# ---------------------------------------------------------------------------

class AlightGroupQuerySetViewTest(TestCase):
    """AlightGroupQuerySetView renders grouped HTML fragments.

    Uses the self-referential ``test`` FK on alight_foreign_key.TModel so
    that no additional model is needed.  Parent objects become the group
    labels; children become the grouped items.
    """

    def setUp(self):
        self.TModel = get_tmodel()
        self.parent = self.TModel.objects.create(name='parent_grp')
        self.child1 = self.TModel.objects.create(name='child_a', test=self.parent)
        self.child2 = self.TModel.objects.create(name='child_b', test=self.parent)
        self.factory = RequestFactory()

    def _view_class(self):
        class GroupedView(AlightGroupQuerySetView):
            group_by_related = 'test'
            related_field_name = 'name'
            search_fields = ['name']
        return GroupedView

    def _get(self, q=''):
        view = self._view_class().as_view(model=self.TModel)
        request = self.factory.get('/', {'q': q})
        request.user = User()
        return view(request)

    def test_group_header_rendered(self):
        r = self._get(q='child')
        self.assertIn('autocomplete-light-group', r.content.decode())

    def test_group_header_contains_parent_name(self):
        r = self._get(q='child')
        self.assertIn('parent_grp', r.content.decode())

    def test_items_in_group_have_data_value(self):
        r = self._get(q='child')
        content = r.content.decode()
        self.assertIn('data-value="%s"' % self.child1.pk, content)
        self.assertIn('data-value="%s"' % self.child2.pk, content)

    def test_content_type_is_html(self):
        r = self._get(q='child')
        self.assertEqual(r['Content-Type'], 'text/html; charset=utf-8')

    def test_raises_without_group_by_related(self):
        from django.core.exceptions import ImproperlyConfigured
        view = AlightGroupQuerySetView.as_view(model=self.TModel)
        request = self.factory.get('/')
        request.user = User()
        with self.assertRaises(ImproperlyConfigured):
            view(request)


# ---------------------------------------------------------------------------
# AlightGroupListView
# ---------------------------------------------------------------------------

class AlightGroupListViewTest(TestCase):
    """AlightGroupListView renders grouped HTML fragments from a list."""

    class CountryView(AlightGroupListView):
        def get_list(self):
            return [
                ('Europe', 'France'),
                ('Europe', 'Germany'),
                ('Asia', 'Japan'),
                ('Asia', 'China'),
                'Ungrouped',
            ]

    class TupleValueView(AlightGroupListView):
        def get_list(self):
            return [
                ('Fruit', ('a', 'Apple')),
                ('Fruit', ('b', 'Banana')),
            ]

    def _get(self, view_cls, q=''):
        factory = RequestFactory()
        request = factory.get('/', {'q': q})
        request.user = get_user_model()()
        return view_cls.as_view()(request)

    def test_group_header_rendered(self):
        r = self._get(self.CountryView)
        self.assertIn('autocomplete-light-group', r.content.decode())

    def test_group_header_text(self):
        r = self._get(self.CountryView)
        content = r.content.decode()
        self.assertIn('Europe', content)
        self.assertIn('Asia', content)

    def test_items_under_group(self):
        r = self._get(self.CountryView)
        content = r.content.decode()
        self.assertIn('data-value="France"', content)
        self.assertIn('data-value="Japan"', content)

    def test_ungrouped_items_appear_first(self):
        r = self._get(self.CountryView)
        content = r.content.decode()
        # 'Ungrouped' should appear before any group header
        ungrouped_pos = content.index('Ungrouped')
        group_pos = content.index('autocomplete-light-group')
        self.assertLess(ungrouped_pos, group_pos)

    def test_filters_by_query(self):
        r = self._get(self.CountryView, q='Fran')
        content = r.content.decode()
        self.assertIn('France', content)
        self.assertNotIn('Germany', content)
        self.assertNotIn('Japan', content)

    def test_tuple_value_label(self):
        r = self._get(self.TupleValueView)
        content = r.content.decode()
        self.assertIn('data-value="a"', content)
        self.assertIn('Apple', content)

    def test_content_type_is_html(self):
        r = self._get(self.CountryView)
        self.assertEqual(r['Content-Type'], 'text/html; charset=utf-8')


# ---------------------------------------------------------------------------
# AlightListView POST edge cases
# ---------------------------------------------------------------------------

class AlightListViewPostEdgeCasesTest(TestCase):
    class ViewWithCreate(AlightListView):
        def get_list(self):
            return ['a', 'b']

        def create(self, text):
            return None  # simulate failure

    def test_post_missing_text_returns_400(self):
        factory = RequestFactory()
        request = factory.post('/', {})  # no 'text' key
        request.user = get_user_model()()
        r = self.ViewWithCreate.as_view()(request)
        self.assertEqual(r.status_code, 400)

    def test_post_create_returns_none_gives_400(self):
        factory = RequestFactory()
        request = factory.post('/', {'text': 'new_value'})
        request.user = get_user_model()()
        r = self.ViewWithCreate.as_view()(request)
        self.assertEqual(r.status_code, 400)

    def test_post_without_create_method_returns_405(self):
        class PlainView(AlightListView):
            def get_list(self):
                return ['a']

        factory = RequestFactory()
        request = factory.post('/', {'text': 'x'})
        request.user = get_user_model()()
        response = PlainView.as_view()(request)
        self.assertEqual(response.status_code, 405)


# ---------------------------------------------------------------------------
# TaggitAlight widget
# ---------------------------------------------------------------------------

class TaggitAlightTest(TestCase):
    """TaggitAlight differences from TagAlight."""

    def _widget(self):
        return TaggitAlight(url='/tag-autocomplete/')

    def test_single_tag_gets_trailing_comma(self):
        w = self._widget()
        # Simulate a single-tag submission (no comma yet).
        data = {'tags': ['multi word tag']}
        result = w.value_from_datadict(data, {}, 'tags')
        # Should end with a comma so taggit parses "multi word tag" as one tag.
        self.assertTrue(result.endswith(','), repr(result))

    def test_multi_tag_no_trailing_comma_added(self):
        w = self._widget()
        data = {'tags': ['foo', 'bar']}
        result = w.value_from_datadict(data, {}, 'tags')
        # Already comma-joined by super(); trailing comma only added for singles.
        self.assertIn(',', result)
        # Count commas: "foo,bar" has one comma, which is not a trailing comma.
        self.assertEqual(result, 'foo,bar')

    def test_option_value_plain_string(self):
        w = self._widget()
        self.assertEqual(w.option_value('django'), 'django')

    def test_option_value_tagged_item(self):
        """option_value should unwrap TaggedItem-like objects via .tag.name."""

        class FakeTag:
            name = 'python'

        class FakeTaggedItem:
            tag = FakeTag()

        w = self._widget()
        self.assertEqual(w.option_value(FakeTaggedItem()), 'python')

    def test_empty_value_unchanged(self):
        w = self._widget()
        data = {'tags': []}
        result = w.value_from_datadict(data, {}, 'tags')
        self.assertEqual(result, '')

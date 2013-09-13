from .case import *

from django.contrib.auth.models import User


class AutocompleteModelMock(autocomplete_light.AutocompleteModelBase):
    limit_choices = 2
    choices = User.objects.all()
    search_fields = ('username', 'email')


class FormMock(forms.Form):
    x = forms.ModelChoiceField(queryset=AutocompleteModelMock.choices,
        widget=autocomplete_light.ChoiceWidget(
            autocomplete=AutocompleteModelMock))


class MultipleFormMock(forms.Form):
    x = forms.ModelMultipleChoiceField(queryset=AutocompleteModelMock.choices,
        widget=autocomplete_light.MultipleChoiceWidget(
            autocomplete=AutocompleteModelMock))


class AutocompleteModelTestCase(AutocompleteTestCase):
    autocomplete_mock = AutocompleteModelMock

    def setUp(self):
        User.objects.all().delete()
        self.abe = User(username='Abe', email='sales@example.com')
        self.jack = User(username='Jack', email='jack@example.com')
        self.james = User(username='James', email='sales@example.com')
        self.john = User(username='John', email='sales@example.com')

        self.abe.save()
        self.jack.save()
        self.james.save()
        self.john.save()

    def assert_choices_equal(self, result, test):
        self.assertEqual(list(result), test['expected'])

    def get_choices_for_values_tests(self):
        return (
            {
                'fixture': [1, 4],
                'expected': [
                    self.abe,
                    self.john,
                ]
            },
        )

    def get_choices_for_request_tests(self):
        return (
            {
                'fixture': make_get_request('q=j'),
                'kwargs': {
                    'limit_choices': 5,
                },
                'expected': [
                    self.jack,
                    self.james,
                    self.john,
                ]
            },
            {
                'fixture': make_get_request('q=j'),
                'kwargs': {
                    'order_by': '-username',
                    'limit_choices': 5,
                },
                'expected': [
                    self.john,
                    self.james,
                    self.jack,
                ]
            },
            {
                'fixture': make_get_request('q=j'),
                'kwargs': {
                    'order_by': ('-email', 'username'),
                    'limit_choices': 5,
                },
                'expected': [
                    self.james,
                    self.john,
                    self.jack,
                ]
            },
            {
                'fixture': make_get_request('q=sale'),
                'expected': [
                    self.abe,
                    self.james,
                ]
            },
            {
                'fixture': make_get_request(),
                'expected': [
                    self.abe,
                    self.jack,
                ]
            },
        )

    def get_validate_tests(self):
        return (
            {
                'fixture': [1, 4],
                'expected': True,
            },
            {
                'fixture': [1, 4, 123],
                'expected': False,
            },
        )

    def get_autocomplete_html_tests(self):
        return (
            {
                'fixture': make_get_request('q=j'),
                'expected': u''.join([
                    '<span class="div" data-value="%s">%s</span>' % (
                        self.jack.pk, unicode(self.jack)),
                    '<span class="div" data-value="%s">%s</span>' % (
                        self.james.pk, unicode(self.james)),
                ])
            },
            {
                'fixture': make_get_request(),
                'expected': u''.join([
                    '<span class="div" data-value="%s">%s</span>' % (
                        self.abe.pk, unicode(self.abe)),
                    '<span class="div" data-value="%s">%s</span>' % (
                        self.jack.pk, unicode(self.jack)),
                ])
            },
        )

    def get_widget_tests(self):
        return (
            {
                'form_class': FormMock,
                'fixture': 'x=4',
                'expected_valid': True,
                'expected_data': self.john,
            },
            {
                'form_class': FormMock,
                'fixture': 'x=3&x=4',
                'expected_valid': True,
                'expected_data': self.john,
            },
            {
                'fixture': 'x=abc',
                'expected_valid': False,
            },
            {
                'form_class': MultipleFormMock,
                'fixture': 'x=4&x=2',
                'expected_valid': True,
                'expected_data': [self.jack, self.john],
            },
            {
                'fixture': 'x=abc&x=2',
                'expected_valid': False,
            },
        )

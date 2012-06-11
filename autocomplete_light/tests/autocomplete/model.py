from .case import *

from django.contrib.auth.models import User


class AutocompleteModelMock(autocomplete_light.AutocompleteModelBase):
    limit_choices = 2
    choices = User.objects.all()
    search_fields = ('username', 'email')


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
                'expected': [
                    self.jack,
                    self.james,
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
            }
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
            {
                'fixture': ['bla'],
                'expected': False,
            },
        )

    def get_autocomplete_html_tests(self):
        return (
            {
                'fixture': make_get_request('q=j'),
                'expected': u''.join([
                    '<div data-value="%s">%s</div>' % (
                        self.jack.pk, unicode(self.jack)),
                    '<div data-value="%s">%s</div>' % (
                        self.james.pk, unicode(self.james)),
                ])
            },
            {
                'fixture': make_get_request(),
                'expected': u''.join([
                    '<div data-value="%s">%s</div>' % (
                        self.abe.pk, unicode(self.abe)),
                    '<div data-value="%s">%s</div>' % (
                        self.jack.pk, unicode(self.jack)),
                ])
            },
        )

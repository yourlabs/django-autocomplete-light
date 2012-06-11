from .case import *

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group


class AutocompleteGenericMock(autocomplete_light.AutocompleteGenericBase):
    choices = (
        User.objects.filter(pk__lt=10),
        Group.objects.filter(pk__lt=10),
    )
    search_fields = (
        ('username', 'email'),
        ('name',),
    )
    limit_choices = 3


class AutocompleteGenericTestCase(AutocompleteTestCase):
    autocomplete_mock = AutocompleteGenericMock

    def setUp(self):
        self.user_ctype = ContentType.objects.get_for_model(User)
        self.group_ctype = ContentType.objects.get_for_model(Group)

        User.objects.all().delete()
        self.abe = User(username='Abe', email='sales@example.com')
        self.jack = User(username='Jack', email='jack@example.com')
        self.james = User(username='James', email='sales@example.com')
        self.john = User(username='John', email='sales@example.com')
        self.elton = User(username='Elton', email='elton@example.com', pk=10)

        self.abe.save()
        self.jack.save()
        self.james.save()
        self.john.save()

        Group.objects.all().delete()
        self.rockers = Group(name='rockers')
        self.bluesmen = Group(name='bluesmen')
        self.jazzmen = Group(name='jazzmen')
        self.emos = Group(name='emos', pk=10)

        self.rockers.save()
        self.bluesmen.save()
        self.jazzmen.save()
        self.emos.save()

    def assert_choices_equal(self, result, test):
        self.assertEqual(list(result), test['expected'])

    def get_choices_for_values_tests(self):
        return (
            {
                'fixture': [
                    '%s-%s' % (self.user_ctype.pk, self.james.pk),
                    '%s-%s' % (self.group_ctype.pk, self.bluesmen.pk),
                ],
                'expected': [
                    self.james,
                    self.bluesmen,
                ]
            },
            {
                'fixture': [
                    '%s-%s' % (self.user_ctype.pk, self.james.pk),
                    '%s-%s' % (self.user_ctype.pk, self.elton.pk),
                    '%s-%s' % (self.group_ctype.pk, self.bluesmen.pk),
                    '%s-%s' % (self.group_ctype.pk, self.emos.pk),
                ],
                'expected': [
                    self.james,
                    self.bluesmen,
                ],
                'name': 'should ignore values that are not in the querysets',
            },
        )

    def get_choices_for_request_tests(self):
        return (
            {
                'fixture': make_get_request('j'),
                'expected': [
                    self.abe,
                    self.rockers,
                    self.bluesmen,
                ],
            },
            {
                'fixture': make_get_request('q=elton'),
                'expected': [],
                'name': 'should not propose models that are not in the qs',
            },
        )

    def get_validate_tests(self):
        return (
            {
                'fixture': [
                    '%s-%s' % (self.user_ctype.pk, self.james.pk),
                    '%s-%s' % (self.group_ctype.pk, self.bluesmen.pk),
                    '%s-%s' % (self.group_ctype.pk, self.emos.pk),
                ],
                'expected': False,
            },
            {
                'fixture': [
                    '%s-%s' % (self.user_ctype.pk, self.james.pk),
                    '%s-%s' % (self.group_ctype.pk, self.bluesmen.pk),
                ],
                'expected': True,
            },
            {
                'fixture': [],
                'expected': True,
            },
            {
                'fixture': ['bla'],
                'expected': False,
            },
            {
                'fixture': ['123123-123123'],
                'expected': False,
            },
        )

    def get_autocomplete_html_tests(self):
        return []

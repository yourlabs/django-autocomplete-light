from ...example_apps.music.models import Artist, Genre
from .case import *


class AutocompleteModelMock(autocomplete_light.AutocompleteModelBase):
    limit_choices = 2
    choices = Artist.objects.all()
    search_fields = ('name', 'genre__name')


class AutocompleteSearchFieldsTestCase(AutocompleteTestCase):
    autocomplete_mock = AutocompleteModelMock

    def setUp(self):
        def create(cls, name, genre=None):
            m = cls(name=name)

            if genre is not None:
                m.genre = genre

            m.save()
            return m

        Artist.objects.all().delete()
        Genre.objects.all().delete()

        self.blues = create(Genre, 'Blues')
        self.buddy_guy = create(Artist, 'Buddy Guy', self.blues)
        self.muddy_waters = create(Artist, 'Muddy Watters', self.blues)

        # Create some noise, those should not appear in results
        self.rock_n_roll = create(Genre, 'Rock\'n\'roll')
        self.chuck_berry = create(Artist, 'Chuck Berry', self.rock_n_roll)

    def get_choices_for_request_tests(self):
        return (
            # First do some tests on search_fields with a one-word query
            {
                'fixture': make_get_request('q=bud'),
                'kwargs': dict(
                    search_fields=('^name', '^genre__name')
                ),
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=ues'),
                'kwargs': dict(
                    search_fields=('^name', '^genre__name')
                ),
                'expected': []
            },
            {
                'fixture': make_get_request('q=watters'),
                'expected': [
                    self.muddy_waters,
                ]
            },
            {
                'fixture': make_get_request('q=watters'),
                'kwargs': dict(
                    search_fields=('^name', '^genre__name')
                ),
                'expected': []
            },
            # Same on a related field
            {
                'fixture': make_get_request('q=Blu'),
                'kwargs': dict(
                    search_fields=('^name', '^genre__name')
                ),
                'expected': [
                    self.buddy_guy,
                    self.muddy_waters,
                ]
            },
            {
                'fixture': make_get_request('q=ues'),
                'expected': [
                    self.buddy_guy,
                    self.muddy_waters,
                ]
            },
            # Now test various split_words options
            {
                'fixture': make_get_request('q=buddy gu'),
                'kwargs': dict(
                    search_fields=('^name', '^genre__name')
                ),
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=buddy gu'),
                'kwargs': dict(
                    split_words='or',
                    search_fields=('^name', '^genre__name')
                ),
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=buddy gu'),
                'kwargs': dict(
                    split_words=True,
                    search_fields=('^name', '^genre__name')
                ),
                'expected': [
                ]
            },
            {
                'fixture': make_get_request('q=bud bl'),
                'kwargs': dict(
                    search_fields=('^name', '^genre__name')
                ),
                'expected': [
                ]
            },
            {
                'fixture': make_get_request('q=bud bl'),
                'kwargs': dict(
                    split_words=True,
                    search_fields=('^name', '^genre__name')
                ),
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=bud bl'),
                'kwargs': dict(
                    split_words='or',
                    search_fields=('^name', '^genre__name')
                ),
                'expected': [
                    self.buddy_guy,
                    self.muddy_waters,
                ]
            },
        )


class AutocompleteGenericMock(autocomplete_light.AutocompleteGenericBase):
    limit_choices = 6
    choices = (
        Artist.objects.all(),
        Genre.objects.all(),
    )
    search_fields = (
        ('name', 'genre__name'),
        ('name',),
    )


class AutocompleteGenericSearchFieldsTestCase(AutocompleteSearchFieldsTestCase):
    autocomplete_mock = AutocompleteGenericMock

    def get_choices_for_request_tests(self):
        return (
            # First do some tests on search_fields with a one-word query
            {
                'fixture': make_get_request('q=bud'),
                'kwargs': dict(
                    search_fields=(('^name', '^genre__name'), ('^name',))
                ),
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=ues'),
                'kwargs': dict(
                    search_fields=(('^name', '^genre__name'), ('^name',))
                ),
                'expected': [
                ]
            },
            {
                'fixture': make_get_request('q=ues'),
                'expected': [
                    self.buddy_guy,
                    self.muddy_waters,
                    self.blues,
                ]
            },
            {
                'fixture': make_get_request('q=watters'),
                'expected': [
                    self.muddy_waters,
                ]
            },
            {
                'fixture': make_get_request('q=watters'),
                'kwargs': dict(
                    search_fields=(('^name', '^genre__name'), ('^name',))
                ),
                'expected': []
            },
            ## Same on a related field
            {
                'fixture': make_get_request('q=Blu'),
                'kwargs': dict(
                    search_fields=(('^name', '^genre__name'), ('^name',))
                ),
                'expected': [
                    self.buddy_guy,
                    self.muddy_waters,
                    self.blues,
                ]
            },
            {
                'fixture': make_get_request('q=ues'),
                'expected': [
                    self.buddy_guy,
                    self.muddy_waters,
                    self.blues,
                ]
            },
            ## Now test various split_words options
            {
                'fixture': make_get_request('q=buddy gu'),
                'kwargs': dict(
                    search_fields=(('^name', '^genre__name'), ('^name',))
                ),
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=buddy gu'),
                'kwargs': dict(
                    split_words='or',
                    search_fields=(('^name', '^genre__name'), ('^name',))
                ),
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=buddy gu'),
                'kwargs': dict(
                    split_words=True,
                    search_fields=(('^name', '^genre__name'), ('^name',))
                ),
                'expected': [
                ]
            },
            {
                'fixture': make_get_request('q=bud bl'),
                'expected': [
                ]
            },
            {
                'fixture': make_get_request('q=bud bl'),
                'kwargs': dict(
                    search_fields=(('^name', '^genre__name'), ('^name',))
                ),
                'expected': [
                ]
            },
            {
                'fixture': make_get_request('q=bud bl'),
                'kwargs': dict(
                    split_words=True,
                    search_fields=(('^name', '^genre__name'), ('^name',))
                ),
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=bud bl'),
                'kwargs': dict(
                    split_words='or',
                    search_fields=(('^name',), ('^name',))
                ),
                'expected': [
                    self.buddy_guy,
                    self.blues,
                ]
            },
            {
                'fixture': make_get_request('q=bud bl'),
                'kwargs': dict(
                    split_words='or',
                    search_fields=(('^name', '^genre__name'), ('^name',))
                ),
                'expected': [
                    self.buddy_guy,
                    self.muddy_waters,
                    self.blues,
                ]
            },
        )

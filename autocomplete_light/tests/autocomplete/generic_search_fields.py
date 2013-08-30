from .case import *

from ..models import Artist, Genre


class AutocompleteModelMock(autocomplete_light.AutocompleteModelBase):
    limit_choices = 2
    choices = Artist.objects.all()
    search_fields = ('^name', '^genre__name')


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

    def get_choices_for_request_tests(self):
        return (
            {
                'fixture': make_get_request('q=Blu'),
                'expected': [
                    self.buddy_guy,
                    self.muddy_waters,
                ]
            },
            {
                'fixture': make_get_request('q=ues'),
                'expected': []
            },
            {
                'fixture': make_get_request('q=watters'),
                'expected': []
            },
            {
                'fixture': make_get_request('q=buddy gu'),
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=bud'),
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=bud bl'),
                'kwargs': {'split_words': True},
                'expected': [
                    self.buddy_guy,
                ]
            },
            {
                'fixture': make_get_request('q=Mud'),
                'expected': [
                    self.muddy_waters,
                ]
            },
        )

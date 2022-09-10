

class AutocompleteFieldMixin(object):
    def __init__(self, field_name=None, view=None, view_cls=None,
                 view_kwargs=None, **kwargs):
        self.field_name = field_name or id(self)
        self.view = view
        self.view_cls = view_cls
        self.view_kwargs = view_kwargs or dict()
        super().__init__(*args, **kwargs)

    def as_url(self, form):
        """
        Create a URL for an autocomplete field.

        :param form: Form class for which to create the url.
        :param field_name: Name of the form attribute for which
        """
        self.view = self.view_cls.as_view(**self.view_kwargs)
        self.url_name = '{}_autocomp_{}'.format(form.__name__, self.name)

        return url(
            r'^{}_{}_autocomp$'.format(form.__name__, self.field_name),
            self.view,
            name=self.url_name,
        )

    def view_kwargs(self):
        return dict()
        return dict(
            model_filters=self.model_filters
        )

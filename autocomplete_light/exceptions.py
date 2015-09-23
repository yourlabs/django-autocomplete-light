class AutocompleteLightException(Exception):
    """ Base Exception for all exceptions of this module. """
    pass


class AutocompleteNotRegistered(AutocompleteLightException):
    """ Attemps to drive the user to debug his registry. """
    def __init__(self, name, registry):
        if registry.keys():
            msg = '%s not registered, you have registered: %s' % (name,
                    list(registry.keys()))
        else:
            msg = '%s not registered (registry is empty)' % name

        super(AutocompleteNotRegistered, self).__init__(msg)


class AutocompleteArgNotUnderstood(AutocompleteLightException):
    """
    Raised by AutocompleteRegistry.get_autocomplete_from_arg when it cannot
    understand the argument.
    """
    def __init__(self, arg, registry):
        msg = '%s not understod by get_autocomplete_from_arg()' % arg
        super(AutocompleteArgNotUnderstood, self).__init__(msg)


class NoGenericAutocompleteRegistered(AutocompleteLightException):
    """
    Raised by AutocompleteRegistry.autocomplete_for_generic when no generic
    autocomplete has been registered.
    """
    def __init__(self, registry):
        msg = 'No generic autocomplete was registered.'
        super(NoGenericAutocompleteRegistered, self).__init__(msg)


class AutocompleteChoicesMustBeQuerySet(AutocompleteLightException):
    """
    Raised by FieldBase constructor when used in conjunction with
    Model(Multiple)ChoiceField given an Autocomplete class which doesn't have a
    QuerySet for the choices attribute.
    """
    def __init__(self, autocomplete):
        msg = ('%s.choices must be a QuerySet to support ModelChoiceField' %
            autocomplete)
        super(AutocompleteChoicesMustBeQuerySet, self).__init__(msg)


class NonDjangoModelSubclassException(AutocompleteLightException):
    pass

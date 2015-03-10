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


class UnconfiguredSearchFieldsException(Exception):
    """
    Raised by :func:`AutocompleteRegistry._register_model_autocomplete` when no
    :attr:`search_fields` were provided and could not be determined
    automatically.
    """
    pass


class NoGenericAutocompleteRegistered(AutocompleteLightException):
    """
    Raised by AutocompleteRegistry.autocomplete_for_generic when no generic
    autocomplete has been registered.
    """
    def __init__(self, registry):
        msg = 'No generic autocomplete was registered.'
        super(NoGenericAutocompleteRegistered, self).__init__(msg)

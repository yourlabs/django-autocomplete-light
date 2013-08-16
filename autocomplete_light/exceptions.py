class AutocompleteLightException(Exception):
    """ Base Exception for all exceptions of this module. """
    pass


class AutocompleteNotRegistered(AutocompleteLightException):
    """ Attemps to drive the user to debug his registry. """
    def __init__(self, name, registry):
        if registry.keys():
            msg = '%s not registered, you have registered: %s' % (name,
                    registry.keys())
        else:
            msg = '%s not registered (registry is empty)' % name

        super(AutocompleteNotRegistered, self).__init__(msg)

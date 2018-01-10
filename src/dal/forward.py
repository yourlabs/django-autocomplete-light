"""Classes for class-based forward declaration."""


class Forward(object):
    """Base class for autocomplete forward declaration."""

    @property
    def type(self):
        """Forward type. Should be implemented in subclasses."""
        raise NotImplementedError("Please use one of my subclasses")

    def to_dict(self):
        """Convert to dictionary which will be rendered as JSON."""
        return {
            "type": self.type
        }


class Field(Forward):
    """Forward field value.

    The type of the forwarded value from the field is either string, list of
    strings or boolean.

    The following rules are used to deduce forwarded type.

     - If there is only one field in the form or subform with name ``src``
    and this field is a checkbox without ``value`` HTML-attribute,
    then boolean value indicating if this checkbox is checked is forwarded.

     - If there is only one field in the form or subform with name ``src``
    and it has ``multiple`` HTML-attribute, then this field is forwarded as a
    list of strings, containing values from this field.

    - If there are one or more fields in the form with name ``src`` and all of
    them are checkboxes with HTML-attribute ``value`` set the list of strings
    containing checked checkboxes is forwarded.

    - Otherwise ``src`` field value forwarded as a string.

    .. py:attribute:: src

        The name of the form field whose value will be forwarded to a view.

    .. py:attribute:: dst

        The name of the key of the forwarded value from the src field in the
        forwarded dictionary. If this value is ``None``, then the key is
        ``src``.
    """

    type = "field"

    def __init__(self, src, dst=None):
        """Instantiate a forwarded field value."""
        self.src = src
        self.dst = dst

    def to_dict(self):
        """Convert to dictionary which will be rendered as JSON."""
        d = super(Field, self).to_dict()

        d.update(src=self.src)
        if self.dst is not None:
            d.update(dst=self.dst)

        return d


class Const(Forward):
    """Forward arbitrary constant value.

    .. py:attribute:: val

        The value to forward. Must be JSON-serializable.

    .. py:attribute:: dst

        The name of the key of the forwarded value.
    """

    type = "const"

    def __init__(self, val, dst):
        """Instantiate a forwarded constant value."""
        self.val = val
        self.dst = dst

    def to_dict(self):
        """Convert to dictionary which will be rendered as JSON."""
        d = super(Const, self).to_dict()

        d.update(val=self.val)
        d.update(dst=self.dst)

        return d


class JavaScript(Forward):
    """Run registered javascript handler and forward its returned value.

    You can register custom forward handler in your JS code as follows:

    .. code-block:: javascript

    yl.registerForwardHandler("your_handler", function (autocompleteElement) {
        // your code here
    });

    Then if your add ``JavaScript("your_handler", "some_value")`` to your
    forwards declaration, your function will be called, autocomplete field
    HTML element will be passed as ``autocompleteElement`` and returned value
    will be added to forward dictionary with ``some_value`` key.

    .. py:attribute:: handler

    The name of the registered handler.

    .. py:attribute:: dst

    The name of the key of the forwarded value from the src field in the
    forwarded dictionary. If this value is ``None``, then the key is
    ``handler``
    """

    type = "javascript"

    def __init__(self, handler, dst=None):
        self.handler = handler
        self.dst = dst

    def to_dict(self):
        """Convert to dictionary which will be rendered as JSON."""
        d = super(JavaScript, self).to_dict()

        d.update(handler=self.handler)
        d.update(dst=self.dst)

        return d


class Self(Forward):
    """Forward own value.

    The same as :class:`Field`, except that `src` is always this field
    itself.

    .. py:attribute:: dst

    The name of the key of the forwarded value from the src field in the
    forwarded dictionary. If this value is ``None``, then the key is
    ``self``.
    """
    type = "self"

    def __init__(self, dst=None):
        """Instantiate a forwarded field value."""
        self.dst = dst

    def to_dict(self):
        """Convert to dictionary which will be rendered as JSON."""
        d = super(Self, self).to_dict()

        if self.dst is not None:
            d.update(dst=self.dst)

        return d

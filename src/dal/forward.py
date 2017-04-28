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


class FieldStrategy(object):
    """
    Enumeration with possible forward strategies for :py:class:`Field`.

    In most cases your fields should be forwarded correctly using ``AUTO``
    strategy which is passed to the :py:class:`Field` constructor as the default
    value. If you're seeing forwarded values of wrong types in your
    autocomplete view (e. g. bool value instead of list) then you should read
    further.

    To get forwarded value DAL does the following:

    - finds forwarded field(s) by name in DOM,
    - serializes fields' value using
        `jQuery.serializeArray <https://api.jquery.com/serializeArray/>`_,
        (note that implementation may change in future releases but
        this function should remain good enough for the purpose of this text)
    - based on selected strategy extracts forwarded value itself to pass
        it to the DAL view.

    So let's assume we have this pseudocode that does first two steps
    and explain all the possible strategies in terms of this pseudocode::

        // List of found fields (jQuery object)
        var fields = findFieldsByName(forwarded);

        // List of javascript objects:
        // [
        //   {
        //       "name": "forwarded",
        //       "value": "val1"
        //   },
        //   {
        //       "name": "forwarded",
        //       "value": "val2"
        //   },
        //   ...
        // ]
        var serializedData = $(fields).serializeArray();

    SINGLE
    ------

    When the ``SINGLE`` strategy is used the value forwarded to the DAL view
    is the value attribute of the first element of ``serializedData``.

    Pseudocode::

        val forwardedValue = serializedData[0].value;

    MULTIPLE
    --------

    When the ``MULTIPLE`` strategy is used the value forwarded to the DAL view
    is the value attribute of the first element of ``serializedData``.

    Pseudocode::

        val forwardedValue = serializedData.map(
            function (item) { return getValueOf(item); }
        );

    EXISTS
    ------

    When the ``EXISTS`` strategy is used the value forwarded to the DAL view
    is boolean ``true`` if ``serializedData`` is not empty, ``false`` otherwise.

    Pseudocode::

        val forwardedValue = serializedData.map(
            function (item) { return getValueOf(item); }
        );


    AUTO
    ----

    When the ``AUTO`` strategy is used the forward strategy for the field
    is deduced automatically based on ``fields`` size and type of each field
    in ``fields``.

    If the length of ``fields`` is 1 and this field has ``multiple`` HTML
    attribute, then ``MULTIPLE`` strategy is used.

    If the length of ``fields`` is more than 1 and all the fields are
    checkboxes, then ``MULTIPLE`` strategy is used.

    If the length of ``fields`` is 1 and the field is checkbox, then
    ``EXISTS`` strategy is used.

    Otherwise ``SINGLE`` strategy is used.
    """
    AUTO = None
    SINGLE = "single"
    MULTIPLE = "multiple"
    EXISTS = "exists"


class Field(Forward):
    """Forward field value.

    .. py:attribute:: src

        The name of the form field whose value will be forwarded to a view.

    .. py:attribute:: dst

        The name of the key of the forwarded value from the src field in the
        forwarded dictionary. If this value is ``None``, then the key is
        ``src``.

    .. py:attribute:: strategy
        The strategy to forward this field. In most cases you should be happy
        with FieldStrategy.AUTO which is passed to the constructor as the
        default value. If you're seeing forwarded values of wrong types (e. g.
        bool value instead of list) in your autocomplete view then you should
        read :py:class:`FieldStrategy` docstring to fine-tune forwarding of
        this field.
    """

    type = "field"

    def __init__(self, src, dst=None, strategy=FieldStrategy.AUTO):
        """Instantiate a forwarded field value."""
        self.src = src
        self.dst = dst
        self.strategy = strategy

    def to_dict(self):
        """Convert to dictionary which will be rendered as JSON."""
        d = super(Field, self).to_dict()

        d.update(src=self.src)
        if self.dst is not None:
            d.update(dst=self.dst)

        if self.strategy is not None:
            d.update(strategy=self.strategy)

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

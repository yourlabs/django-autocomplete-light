import autocomplete_light

from models import TableWidget


autocomplete_light.register(TableWidget,
    autocomplete_light.AutocompleteModelTemplate,
    widget_template='tablewidget_widget.html',
    choice_template='tablewidget_choice.html',
    autocomplete_template='tablewidget_autocomplete.html')

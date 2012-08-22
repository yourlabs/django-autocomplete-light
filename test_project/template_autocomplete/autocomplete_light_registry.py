import autocomplete_light

from models import TemplatedChoice

autocomplete_light.register(TemplatedChoice, 
	autocomplete_light.AutocompleteModelTemplate, 
	choice_template='template_autocomplete/templated_choice.html')
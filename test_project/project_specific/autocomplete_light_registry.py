import autocomplete_light

from models import Contact

autocomplete_light.register(Contact, search_name='name')

from generic_channel_example import *

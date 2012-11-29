Быстрый старт
-------------

#. Подключить библиотеку django_autocomplete_light в зависимости виртуального окружения::

  git+git@github.com:balmaster/django-autocomplete-light.git#egg=django-autocomplete-light

#. Добавить приложение autocomplete_light в ``INSTALLED_APPS``

#. В своем приложении сделать autocomplete_light_registry.py::

  import autocomplete_light

  from .models import *

  autocomplete_light.register(МодельОбъектыКоторойБудутПоказанеВСпискеАвтозавершения, search_fields=('ПоляПоКоторымБудетПоиск',),
    autocomplete_js_attributes={'placeholder': 'ПодсказкаКоторуюУвидитПользователь'})

#. В admin.py надо перехватить генерацию формы для тех форм для кторых должен работать автокомплит::

  import autocomplete_light

  class МодельВФормеКоторойХотимИспользоватьПоляСАвтокомплитомAdmin(...):
    form = autocomplete_light.modelform_factory(МодельВФормеКоторойХотимИспользоватьПоляСАвтокомплитом)
    
Это все, перерь при редактировании МодельВФормеКоторойХотимИспользоватьПоляСАвтокомплитом
если в ней есть поля типа МодельОбъектыКоторойБудутПоказанеВСпискеАвтозавершения они автоматически 
начнут поддерживать автодополнение      
    

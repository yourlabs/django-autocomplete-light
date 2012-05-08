Using autocompletes in forms
============================

Before getting started, make sure you have read about channels, the channel
registry, widgets and forms. It's okay if you don't understand it fully as
we'll go into details in that chapter.

Rather than demonstrating high level usage of this app, this chapter is written
to teach you everything in this app from the ground up.

Register a channel
------------------

Consider a app, 'books', with a Book and an Author model, where Book.author is
a ForeignKey to Author.

Django's ModelForm creates a ModelChoiceField for the author field of Book. By
default, the widget for ModelChoiceField is a Select. If we want to override that to
use an AutocompleteWidget, then we have to register a channel for the Author
model.

In books/autocomplete_light_registry.py, you could do as little as::

    import autocomplete_light

    from models import Author

    autocomplete_light.register(Author)

This will register a channel called AuthorChannel, that's simply a ChannelBase
with model=Author. Like with ModelAdmins, you could register a particular
channel for one or several particular models. Here's an example to filter
objects based on the request user::
 
    import autocomplete_light

    from models import Author, Book

    class UserChannel(autocomplete_light.ChannelBase):
        def get_queryset(self):
            qs = self.model.objects.all()

            request = getattr(self, request, None)
            if request:
                qs = qs.filter(created_by=request.user)

            return qs

    autocomplete_light.register(Author, UserChannel)
    autocomplete_light.register(Book, UserChannel)

Go ahead and read the code of channel.base.ChannelBase, it's simple and
concise. You'll find what you can do. Here are a few things worth mentionning
so that you don't end up pulling your hair off:

- channels are registered as class
- channels are instanciated before they can be used
- when ChannelView instanciates a channel to render the autocomplete, it calls
  the channel method init_for_request
- when the widget instanciates a channel to validate values (selected model
  ids), it does not call init_for_request because it doesn't have the request
  instance, however it does call are_valid()
- the channel name is composed of the model name + the base channel class name

Discover channels
-----------------

Of course, books.autocomplete_light_registry should be imported at some point,
or we'll never know about your channels.

And obviously, before books.admin as books.admin might use forms that have
autocompletes.

In your root url configuration, likely project_root/urls.py, add
autocomplete_light.autodiscover() as such::

    import autocomplete_light
    autocomplete_light.autodiscover()

    from django.contrib import admin
    admin.autodiscover()

Using AutocompleteWidget
------------------------

As mentionned in the design documentation, two options are really important:

- channel_name: the name of the channel that the widget should use
- max_items: the number of items the user can select

Consider such a model::

    class Task(models.Model):
        name = models.CharField(max_length=200)
        
        parent = ForeignKey('Task', null=True, blank=False, related_name='sub_task_set')
        dependencies = models.ManyToManyField('Task', related_name='blocked_tasks_set', blank=True)

Assuming you've registered a channel for Task as such::

    import autocomplete_light

    from models import Task

    autocomplete_light.register(Task)


This model is interresting because it contains both a ForeignKey and a
ManyToManyField. This is how you could make a ModelForm for this model in tasks/forms.py::

    from django import forms

    import autocomplete_light

    from models import Task

    class TaskForm(forms.ModelForm):
        class Meta:
            model = Task
         
        parent = forms.ModelChoiceField(Task.objects.all(),
            widget=autocomplete_light.AutocompleteWidget(channel_name='TaskChannel', max_items=1))
         
        dependencies = forms.ModelMultipleChoiceField(Task.objects.all(),
            widget=autocomplete_light.AutocompleteWidget(channel_name='TaskChannel'))

But in reality, you could just use autocomplete_light.modelform_factory and
obtain the same result::

    import autocomplete_light

    from models import Task

    TaskForm = autocomplete_light.modelform_factory(Task)

Which is the same as::

    from django.forms.models import modelform_factory

    import autocomplete_light

    from models import Task

    TaskForm = modelform_factory(Task, widgets=autocomplete_light.get_widgets_dict(Task))

Templating the autocomplete
---------------------------

The default template is autocomplete_light/autocomplete.html. That said, it
will try autocomplete_light/ChannelName/autocomplete.html

Basically, this means that if you copy autocomplete_light/autocomplete.html to
yourproject/templates/autocomplete_light/AuthorChannel/autocomplete.html, then
you should be able to customize the design of the Author autocomplete.

Note that this template calls channel.result_as_html to render a result. The
reason a result should be rendered individually by a channel is that it must be
rendered by both the autocomplete, but also the deck. The deck is the list of
selected options. You'll see it when the widget is rendered with initial values.

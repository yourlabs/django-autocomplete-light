from django.views.generic.edit import CreateView
from models import TaggitDemo
from forms import TaggitDemoForm

class TaggitDemoCreate(CreateView):
    model = TaggitDemo
    form_class = TaggitDemoForm


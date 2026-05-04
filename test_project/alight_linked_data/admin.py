from django.contrib import admin

from .forms import TForm
from .models import Group, TModel


class TestAdmin(admin.ModelAdmin):
    form = TForm


admin.site.register(Group)
admin.site.register(TModel, TestAdmin)

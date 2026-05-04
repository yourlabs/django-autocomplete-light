from django.contrib import admin

from .forms import TForm
from .models import TModel


class TestAdmin(admin.ModelAdmin):
    form = TForm


admin.site.register(TModel, TestAdmin)

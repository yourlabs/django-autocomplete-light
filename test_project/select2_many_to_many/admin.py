from django.contrib import admin

from .forms import TestForm
from .models import TestModel


class TestInline(admin.TabularInline):
    form = TestForm
    model = TestModel
    fk_name = 'for_inline'


class TestAdmin(admin.ModelAdmin):
    form = TestForm
    inlines = [TestInline]
admin.site.register(TestModel, TestAdmin)

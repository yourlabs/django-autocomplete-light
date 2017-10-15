from django.contrib import admin

import nested_admin

from .forms import TFormThree
from .models import TModelOne, TModelThree, TModelTwo


class TModelThreeInline(nested_admin.NestedStackedInline):
    model = TModelThree
    form = TFormThree
    extra = 1


class TModelTwoInline(nested_admin.NestedStackedInline):
    model = TModelTwo
    inlines = [TModelThreeInline]
    extra = 1


class TModelOneAdmin(nested_admin.NestedModelAdmin):
    model = TModelOne
    inlines = [TModelTwoInline]


admin.site.register(TModelOne, TModelOneAdmin)

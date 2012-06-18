from django.contrib import admin

from forms import OptionnalTaggedItemForm
from models import OptionnalTaggedItem


class OptionnalTaggedItemAdmin(admin.ModelAdmin):
    form = OptionnalTaggedItemForm
admin.site.register(OptionnalTaggedItem, OptionnalTaggedItemAdmin)

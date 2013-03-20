from django.contrib.contenttypes import generic
from django.contrib import admin

from forms import RelationshipForm
from models import Relationship, SomeModel


class RelationshipInline(generic.GenericTabularInline):
    model = Relationship
    extra = 0
    ct_field = "content_type"
    ct_fk_field = "object_id"
    form = RelationshipForm

    def get_formset(self, request, obj=None, **kwargs):
        kwargs.update({'form': RelationshipForm})
        return super(RelationshipInline, self).get_formset(request, obj, **kwargs)


class SomeModelAdmin(admin.ModelAdmin):
    inlines = (
        RelationshipInline,
    )

admin.site.register(SomeModel, SomeModelAdmin)

from django.contrib import admin

from .forms import TestForm
from .models import TestModel


class SecureFormMixin(object):
    def get_form(self, request, obj=None, **kwargs):
        form = super(SecureFormMixin, self).get_form(
            request, obj=obj, **kwargs)

        # Create a copy of the class so that we can hack the field definition
        # safely
        secure_form = type('SecuredAdminForm', (form,), {})

        # Let's secure on the validation side now
        secure_form.base_fields['test'].queryset = TestModel.objects.filter(
            owner=request.user)

        return secure_form


class TestInline(SecureFormMixin, admin.TabularInline):
    fk_name = 'for_inline'
    model = TestModel
    form = TestForm


class TestAdmin(SecureFormMixin, admin.ModelAdmin):
    inlines = [TestInline]
    form = TestForm
admin.site.register(TestModel, TestAdmin)

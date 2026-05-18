from django.contrib import admin

from .forms import TForm
from .models import TModel


class SecureFormMixin:
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj=obj, **kwargs)
        secure_form = type('SecuredAdminForm', (form,), {})
        secure_form.base_fields['test'].queryset = TModel.objects.filter(
            owner=request.user
        )
        return secure_form


class TestInline(SecureFormMixin, admin.TabularInline):
    fk_name = 'for_inline'
    model = TModel
    form = TForm


class TestAdmin(SecureFormMixin, admin.ModelAdmin):
    inlines = [TestInline]
    form = TForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

admin.site.register(TModel, TestAdmin)

from django.contrib import admin

from .forms import OnTheFlyForm
from .models import OnTheFly


class OnTheFlyAdmin(admin.ModelAdmin):
    form = OnTheFlyForm
admin.site.register(OnTheFly, OnTheFlyAdmin)

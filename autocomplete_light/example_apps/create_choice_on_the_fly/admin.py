from django.contrib import admin

from .forms import FlyForm
from .models import Fly


class FlyAdmin(admin.ModelAdmin):
    form = FlyForm
admin.site.register(Fly, FlyAdmin)

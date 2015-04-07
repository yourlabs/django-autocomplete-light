from django.contrib import admin
from django.db import models
from django import forms

from .models import Film
from .forms import FilmForm


class FilmAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ForeignKey: {
            'widget': forms.RadioSelect
        }
    }
    form = FilmForm
admin.site.register(Film, FilmAdmin)

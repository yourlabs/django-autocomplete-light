from django.contrib import admin
from .models import ModelOne, ModelTwo, MasterModel


@admin.register(ModelOne)
class ModelOneAdmin(admin.ModelAdmin):

    list_display = ('name', )


@admin.register(ModelTwo)
class ModelTwoAdmin(admin.ModelAdmin):

    list_display = ('name', )


@admin.register(MasterModel)
class MasterModelAdmin(admin.ModelAdmin):

    list_display = ('name',)
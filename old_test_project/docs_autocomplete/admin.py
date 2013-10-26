from django.contrib import admin

from models import Profile
from forms import ProfileForm


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm

admin.site.register(Profile, ProfileAdmin)

from cities_light.models import City, Country, Region
from django import shortcuts
from django.contrib.auth.models import Group, User
from django.db.models import Q


def navigation_autocomplete(request,
    template_name='navigation_autocomplete/autocomplete.html'):

    q = request.GET.get('q', '')
    context = {'q': q}

    queries = {}
    queries['users'] = User.objects.filter(
        Q(username__icontains=q) |
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(email__icontains=q)
    ).distinct()[:3]
    queries['groups'] = Group.objects.filter(name__icontains=q)[:3]
    queries['cities'] = City.objects.filter(search_names__icontains=q)[:3]
    queries['regions'] = Region.objects.filter(name_ascii__icontains=q)[:3]
    queries['countries'] = Country.objects.filter(name_ascii__icontains=q)[:3]

    context.update(queries)

    return shortcuts.render(request, template_name, context)

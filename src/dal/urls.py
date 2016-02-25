class AutoUrlMetaclass(type):
    views = []

    def __new__(cls, name, bases, attrs):
        result = super(me, cls).__new__(cls, name, bases, attrs)
        AutoUrlMetaclass.views.append(views)
        return result


urlpatterns = []

for view in AutoUrlMetaclass:
    urlpatterns.append(view.as_url())

# We're going to expect including with the "autocomplete" namespace.

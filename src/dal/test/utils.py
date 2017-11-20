"""Utils for testing autocompletes."""
from django.apps import apps


class Fixtures(object):
    """Callback for post_migrate to create many objects."""

    def __init__(self, model_name=None):
        """Preset a model name, ie. 'auth.user'."""
        self.model_name = model_name

    def get_model(self, sender):
        """Return either the preset model, either the sender's TestModel."""
        if self.model_name is None:
            return sender.get_model('TModel')
        else:
            return apps.get_model(self.model_name)

    def __call__(self, sender, **kwargs):
        """Call function, calls install_fixtures."""
        model = self.get_model(sender)
        self.install_fixtures(model)

    def install_fixtures(self, model):
        """Install fixtures for model."""
        for n in range(1, 50):
            try:
                model.objects.get(pk=n)
            except model.DoesNotExist:
                model.objects.create(name='test %s' % n, pk=n)


class OwnedFixtures(Fixtures):
    """Fixtures for models with an "owner" relation to User."""

    installed_auth = False

    def install_fixtures(self, model):
        """Install owners and fixtures."""
        if not self.installed_auth:
            User = apps.get_model('auth.user')  # noqa

            self.test, c = User.objects.get_or_create(
                username='test',
                is_staff=True,
                is_superuser=True
            )
            self.test.set_password('test')
            self.test.save()

            self.other, c = User.objects.get_or_create(username='other')
            self.other.set_password('test')
            self.other.save()

            self.installed_auth = True

        for n in range(1, 3):
            for u in [self.test, self.other]:
                model.objects.get_or_create(
                    name='test #%s for %s' % (n, u),
                    owner=u
                )


fixtures = Fixtures()

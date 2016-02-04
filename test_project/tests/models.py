from django.contrib.auth.models import User
from django.db.models.signals import post_migrate


def test_user(sender, *args, **kwargs):
    if sender.name != 'django.contrib.auth':
        return

    user, c = User.objects.get_or_create(username='test')
    user.is_staff = True
    user.is_superuser = True
    user.set_password('test')
    user.save()

post_migrate.connect(test_user)

from collections import defaultdict
from functools import wraps

import django
import six
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models, transaction
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

# Django 1.5 add support for custom auth user model
if django.VERSION >= (1, 5):
    AUTH_USER_MODEL = settings.AUTH_USER_MODEL
else:
    AUTH_USER_MODEL = 'auth.User'

try:
    atomic = transaction.atomic
except AttributeError:
    from contextlib import contextmanager

    @contextmanager
    def atomic(using=None):
        sid = transaction.savepoint(using=using)
        try:
            yield
        except IntegrityError:
            transaction.savepoint_rollback(sid, using=using)
            raise
        else:
            transaction.savepoint_commit(sid, using=using)


try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey


class VoteManger(models.Manager):
    def filter(self, *args, **kwargs):
        if kwargs.has_key('content_object'):
            content_object = kwargs.pop('content_object')
            content_type = ContentType.objects.get_for_model(content_object)
            kwargs.update({
                    'content_type':content_type,
                    'object_id':content_object.pk
                    })
        return super(VoteManger, self).filter(*args, **kwargs)
    
class Vote(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    create_at = models.DateTimeField(auto_now_add=True)

    objects = VoteManger()
    
    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        app_label = 'unuseable_virtualfield'

    @classmethod
    def votes_for(cls, model, instance=None):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "content_type": ct
        }
        if instance is not None:
            kwargs["object_id"] = instance.pk
            
        return cls.objects.filter(**kwargs)

try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation


def instance_required(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if self.instance is None:
            raise TypeError("Can't call %s with a non-instance manager" % func.__name__)
        return func(self, *args, **kwargs)
    return inner


class VotedQuerySet(QuerySet):
    """
    if call votes.annotate with an `user` argument then add `is_voted` to each instance
    """
    
    def __init__(self, model=None, query=None, using=None, user=None):
        self.user = user
        super(VotedQuerySet, self).__init__(model=model, query=query, using=using)
        
    def __iter__(self):
        super(VotedQuerySet, self).__iter__()
        if self.user is None:
            return iter(self._result_cache)

        objects = self._result_cache
        user_id = self.user.id
        contenttype = ContentType.objects.get_for_model(self.model)
        object_ids = [r.id for r in objects]
        
        voted_users = defaultdict(list)
        votes = Vote.objects.filter(content_type=contenttype, object_id__in=object_ids)
        for v in votes:
            voted_users[v.object_id].append(v.user_id)
            
        for r in objects:
            r.is_voted = user_id in voted_users.get(r.id, [])

        self._result_cache = objects
        return iter(objects)
    
    def _clone(self):
        c = super(VotedQuerySet, self)._clone()
        c.user = self.user
        return c
    
class _VotableManager(models.Manager):
    def __init__(self, through, model, instance, field_name='votes'):
        self.through = through
        self.model = model
        self.instance = instance
        self.field_name = field_name

    @instance_required
    def up(self, user):
        self.through(user=user, content_object=self.instance).save()
        
    @instance_required
    def down(self, user):
        self.through.objects.filter(user=user, content_object=self.instance).delete()

    @instance_required
    def exists(self, user):
        return self.through.objects.filter(user=user, content_object=self.instance).exists()

    def count(self):
        return self.through.votes_for(self.model, self.instance).count()

    def annotate(self, queryset=None, user=None, annotation='num_votes', reverse=True):
        order = reverse and '-%s' % annotation or annotation
        kwargs = {annotation:Count('%s__user' % self.field_name)}
        queryset = queryset if queryset is not None else self.model.objects.all()
        queryset = queryset.annotate(**kwargs).order_by(order, '-id')
        return VotedQuerySet(model=queryset.model, query=queryset.query, user=user)
        
class VotableManager(GenericRelation):
    def __init__(self, through=Vote, manager=_VotableManager, **kwargs):
        self.through = through
        self.manager = manager
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Votes'))
        super(VotableManager, self).__init__(self.through, **kwargs)
        
    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError("%s objects need to have a primary key value "
                "before you can access their votes." % model.__name__)
        manager = self.manager(
            through=self.through,
            model=model,
            instance=instance,
            field_name=self.name
        )
        return manager

    def contribute_to_class(self, cls, name):
        super(VotableManager, self).contribute_to_class(cls, name)
        setattr(cls, name, self)

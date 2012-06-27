from django.db import models

__all__ = ('AutocompleteModelProxy',)


class AutocompleteModelProxy(object):
    get_or_create_fields = {
        'auth.user': ('username',),
        'auth.group': ('name',),
    }

    def choice_dict(self, choice):
        return self.model_dict(choice)

    def choice_dict_value(self, choice):
        return self.model_dict_value(choice).pk

    def model_dict(self, model):
        data = {
            'module_name': model._meta.module_name,
            'app_label': model._meta.app_label,
        }

        for field in model._meta.fields:
            if isinstance(field, models.AutoField):
                continue

            if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                try:
                    related = getattr(model, field.name, None)
                except models.DoesNotExist:
                    continue
                else:
                    data[field.name] = self.model_dict(related)
            else:
                data[field.name] = getattr(model, field.name, None)

        return data

    def _get_or_create_model_from_dict(self, model_dict):
        module_name = model_dict.pop('module_name').lower()
        app_label = model_dict.pop('app_label').lower()
        model_class = models.get_model(app_label, module_name)
        model_code = u'%s.%s' % (app_label, module_name)
        get_or_create_fields = self.get_or_create_fields.get(model_code, None)

        kwargs = {}
        for field in get_or_create_fields:
            if field.name not in model_dict.keys():
                continue

            if isinstance(field, models.DateTimeField):
                # skews caused by precision diference between the database
                # and the serializer make datetime fields a bad choice for
                # get_or_create.
                continue

            kwargs[field.name] = model_dict[field.name]

        model, created = model_class.objects.get_or_create(**kwargs)

        #for key, value in model_dict.items():
            #if isinstance(value, dict):
                #related = self._get_or_create_model_from_dict(value)
                #model_dict[key] = related

        return model

    def dicts_to_model(self, model_dict):
        for key, value in model_dict.items():
            if isinstance(value, dict):
                model_dict[key] = self._get_or_create_model_from_dict(value)

    def model_dict_value(self, model_dict):
        module_name = model_dict.pop('module_name').lower()
        app_label = model_dict.pop('app_label').lower()
        model_class = models.get_model(app_label, module_name)
        model_code = u'%s.%s' % (app_label, module_name)
        get_or_create_fields = self.get_or_create_fields.get(model_code, None)

        # first pass, get or create each
        kwargs = {}
        #for key, value in model_dict.items():

        #model, c = model_class.objects.get_or_create(**kwargs)

        # second pass, finish the model
        for key, value in kwargs.items():
            if isinstance(value, dict):
                setattr(model, key, self.model_dict_value(value))
            else:
                setattr(model, key, value)

        model.save()

        return model

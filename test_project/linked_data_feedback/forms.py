from dal import autocomplete

# Without autocomplete...
# from django.contrib.auth import get_user_model
# from django.forms.widgets import Select


from django import forms

from .models import TestModel


class TestForm(forms.ModelForm):
    def clean_test(self):
        owner = self.cleaned_data.get('owner', None)
        value = self.cleaned_data.get('test', None)

        if value and owner and value.owner != owner:
            raise forms.ValidationError('Wrong owner for test')

        return value

    class Meta:
        model = TestModel
        fields = ('name', 'owner', 'test')
        widgets = {
            'owner': autocomplete.ModelSelect2(
                url='linked_data_feedback_users',
                feedback=('test',)),
            # Or without autocomplete ...
            # 'owner': Select(attrs={
            #     "data-autocomplete-light-forward-feedback": "test"
            # }, choices=get_user_model().objects.all()),
            'test': autocomplete.ModelSelect2(url='linked_data_feedback',
                                              forward=('owner',))
        }

from django.conf.urls import patterns, include, url

from django.views import generic

from forms import ScheduleForm


urlpatterns = patterns('',
    url(r'form/$', generic.FormView.as_view(form_class=ScheduleForm,
        template_name='support_sandino/index.html',
        success_url='success/'), name='support_sandino'),
    url(r'success/', generic.TemplateView.as_view(
        template_name='support_sandino/success.html'),
        name='support_sandino_success'),
)

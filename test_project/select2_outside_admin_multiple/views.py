try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.shortcuts import render


from .forms import Form1, Form2


def multiple_form(request):
    ctx = {}
    ctx['form1'] = Form1()
    ctx['form2'] = Form2()
    if request.method == 'POST':
        form1 = Form1(request.POST)
        form2 = Form2(request.POST)
        if form1.is_valid():
            form1.save()
        if form2.is_valid():
            form2.save()
    return render(request, 'select2_outside_admin_multiple.html', ctx)
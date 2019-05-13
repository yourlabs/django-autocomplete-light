from django.shortcuts import render, get_object_or_404
from .models import TModel
from .forms import EditTForm


def edit_t_model(request, pk):

    """

    without functions added in TaggitSelect2 page will raise exception:
    Tag Object Not Iterable

    """

    tobject = get_object_or_404(TModel, pk=pk)

    if request.method == 'POST':
        main_form = EditTForm(request.POST, instance=tobject)
    else:
        main_form = EditTForm(instance=tobject)

    context = {
        'tobject': tobject,
        'main_form': main_form,
    }
    return render(request, 'edit_t_model.html', context)
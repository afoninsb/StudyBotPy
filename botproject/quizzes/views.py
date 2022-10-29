from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddQuizStep1, AddQuizStep2


def index(request, botid):
    pass


def quiz_add(request, botid, step):
    if step == 1:
        form = AddQuizStep2(request.POST, count=3 or None)
    context = {
        'form': form,
        'step': step,
    }
    return render(request, 'quizzes/quiz_add.html', context)

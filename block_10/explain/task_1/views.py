from django.shortcuts import render

from block_10.explain.task_1.tests import ExplainTest


def index(request):
    """ Начальная загрузка данных """
    #ExplainTest.setUpTestData()

    listTask1 = []

    return render(
            request,
            'explain.html',
            context={
                'listTask1': listTask1
            }
    )
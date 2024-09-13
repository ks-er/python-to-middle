from django.shortcuts import render

from block_10.explain.task_1.implementation import ReportHelper
from block_10.explain.task_1.tests import ExplainTest


def index(request):
    """ Начальная загрузка данных """
    #ExplainTest.setUpTestData()

    popular_books = ReportHelper.get_popular_books_for_month()
    moving_books = ReportHelper.get_popular_moving_books_for_month()

    return render(
            request,
            'explain.html',
            context={
                'popular_books': popular_books,
                'moving_books':moving_books
            }
    )
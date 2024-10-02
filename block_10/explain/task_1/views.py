from django.shortcuts import render

from block_10.explain.task_1.implementation import ReportHelper
from block_10.explain.task_1.tests import ExplainTest


def index(request):
    """Начальная загрузка данных"""
    # ExplainTest.setUpTestData()

    popular_books = ReportHelper.get_popular_books_for_month()
    moving_books = ReportHelper.get_popular_moving_books_for_month()
    active_readers = ReportHelper.get_active_readers()
    overdue_returns = ReportHelper.get_overdue_returns()
    outside_library_readers = ReportHelper.get_outside_library_readers()
    read_pages_by_publication = ReportHelper.get_read_pages_by_publication()
    rooms_info_list = ReportHelper.get_halls_list()
    unpopular_books = ReportHelper.get_unpopular_books()

    return render(
        request,
        "explain.html",
        context={
            "popular_books": popular_books,
            "moving_books": moving_books,
            "active_readers": active_readers,
            "overdue_returns": overdue_returns,
            "outside_library_readers": outside_library_readers,
            "read_pages_by_publication": read_pages_by_publication,
            "rooms_info_list": rooms_info_list,
            "unpopular_books": unpopular_books,
        },
    )

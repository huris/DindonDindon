from django.urls import path, re_path

from Tables.views import TableListView, BookTableView, BookUpdateView, BookTimeListView, \
    BookDestroyView, TableUpdateView, TableRetrieveView

urlpatterns = [
    path('', TableListView.as_view()),
    # 获取某个餐桌的状态
    re_path(r'(?P<pk>\d+)$', TableRetrieveView.as_view()),
    # 修改餐桌状态
    re_path(r'(?P<pk>\d+)/update', TableUpdateView.as_view()),
    path('users', BookTimeListView.as_view()),
    path('books', BookTableView.as_view()),
    # 更新预约
    re_path(r'books/(?P<pk>\d+)/update', BookUpdateView.as_view()),
    # 删除预约
    re_path(r'books/(?P<pk>\d+)/destroy', BookDestroyView.as_view()),
]

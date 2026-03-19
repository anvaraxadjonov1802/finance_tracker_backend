from django.urls import path
from .views import (
    DebtRecordListCreateView,
    DebtRecordRetrieveUpdateDestroyView,
    close_debt_record,
    reopen_debt_record,
)

urlpatterns = [
    path('', DebtRecordListCreateView.as_view(), name='debt-list-create'),
    path('<int:pk>/', DebtRecordRetrieveUpdateDestroyView.as_view(), name='debt-detail'),
    path('<int:pk>/close/', close_debt_record, name='debt-close'),
    path('<int:pk>/reopen/', reopen_debt_record, name='debt-reopen'),
]
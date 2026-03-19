from django.urls import path
from .views import (
    BudgetListCreateView,
    BudgetRetrieveUpdateDestroyView,
    BudgetLimitListCreateView,
    BudgetLimitRetrieveUpdateDestroyView,
    current_budget_view,
)

urlpatterns = [
    path('', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('current/', current_budget_view, name='budget-current'),
    path('<int:pk>/', BudgetRetrieveUpdateDestroyView.as_view(), name='budget-detail'),

    path('<int:budget_id>/limits/', BudgetLimitListCreateView.as_view(), name='budget-limit-list-create'),
    path('<int:budget_id>/limits/<int:pk>/', BudgetLimitRetrieveUpdateDestroyView.as_view(), name='budget-limit-detail'),
]
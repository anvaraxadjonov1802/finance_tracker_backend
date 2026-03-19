from django.urls import path
from .views import (
    analytics_summary_view,
    category_breakdown_view,
    income_vs_expense_trend_view,
    calendar_view,
    budget_vs_actual_view,
)

urlpatterns = [
    path('summary/', analytics_summary_view, name='analytics-summary'),
    path('category-breakdown/', category_breakdown_view, name='analytics-category-breakdown'),
    path('income-vs-expense/', income_vs_expense_trend_view, name='analytics-income-vs-expense'),
    path('calendar/', calendar_view, name='analytics-calendar'),
    path('budget-vs-actual/', budget_vs_actual_view, name='analytics-budget-vs-actual'),
]
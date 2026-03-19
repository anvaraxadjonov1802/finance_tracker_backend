from rest_framework import serializers


class SummarySerializer(serializers.Serializer):
    total_balance = serializers.DecimalField(max_digits=14, decimal_places=2)
    monthly_income = serializers.DecimalField(max_digits=14, decimal_places=2)
    monthly_expense = serializers.DecimalField(max_digits=14, decimal_places=2)
    net_savings = serializers.DecimalField(max_digits=14, decimal_places=2)
    open_debt_total = serializers.DecimalField(max_digits=14, decimal_places=2)
    open_receivable_total = serializers.DecimalField(max_digits=14, decimal_places=2)


class CategoryBreakdownItemSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    percentage = serializers.FloatField()


class TrendItemSerializer(serializers.Serializer):
    period = serializers.CharField()
    income = serializers.DecimalField(max_digits=14, decimal_places=2)
    expense = serializers.DecimalField(max_digits=14, decimal_places=2)
    net = serializers.DecimalField(max_digits=14, decimal_places=2)


class CalendarDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    income = serializers.DecimalField(max_digits=14, decimal_places=2)
    expense = serializers.DecimalField(max_digits=14, decimal_places=2)
    net = serializers.DecimalField(max_digits=14, decimal_places=2)


class BudgetVsActualSerializer(serializers.Serializer):
    budget_id = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    planned_income = serializers.DecimalField(max_digits=14, decimal_places=2)
    actual_income = serializers.DecimalField(max_digits=14, decimal_places=2)
    actual_expense = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_expense_limit = serializers.DecimalField(max_digits=14, decimal_places=2)
    remaining_budget = serializers.DecimalField(max_digits=14, decimal_places=2)
    income_gap = serializers.DecimalField(max_digits=14, decimal_places=2)
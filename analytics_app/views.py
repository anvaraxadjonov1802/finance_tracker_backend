from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.models import Account
from budgets.models import Budget
from debts.models import DebtRecord
from transactions.models import Transaction
from .serializers import (
    SummarySerializer,
    CategoryBreakdownItemSerializer,
    TrendItemSerializer,
    CalendarDaySerializer,
    BudgetVsActualSerializer,
)


def _get_month_and_year(request):
    today = timezone.localdate()
    month = int(request.query_params.get('month', today.month))
    year = int(request.query_params.get('year', today.year))
    return month, year


def _decimal_or_zero(value):
    return value or Decimal('0.00')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics_summary_view(request):
    month, year = _get_month_and_year(request)
    user = request.user

    total_balance = Account.objects.filter(
        user=user,
        is_active=True
    ).aggregate(total=Sum('current_balance'))['total']

    monthly_income = Transaction.objects.filter(
        user=user,
        transaction_type=Transaction.TransactionType.INCOME,
        transaction_date__year=year,
        transaction_date__month=month,
    ).aggregate(total=Sum('amount'))['total']

    monthly_expense = Transaction.objects.filter(
        user=user,
        transaction_type=Transaction.TransactionType.EXPENSE,
        transaction_date__year=year,
        transaction_date__month=month,
    ).aggregate(total=Sum('amount'))['total']

    open_debt_total = DebtRecord.objects.filter(
        user=user,
        debt_type=DebtRecord.DebtType.DEBT,
        status=DebtRecord.Status.OPEN,
    ).aggregate(total=Sum('amount'))['total']

    open_receivable_total = DebtRecord.objects.filter(
        user=user,
        debt_type=DebtRecord.DebtType.RECEIVABLE,
        status=DebtRecord.Status.OPEN,
    ).aggregate(total=Sum('amount'))['total']

    total_balance = _decimal_or_zero(total_balance)
    monthly_income = _decimal_or_zero(monthly_income)
    monthly_expense = _decimal_or_zero(monthly_expense)
    open_debt_total = _decimal_or_zero(open_debt_total)
    open_receivable_total = _decimal_or_zero(open_receivable_total)

    data = {
        'total_balance': total_balance,
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'net_savings': monthly_income - monthly_expense,
        'open_debt_total': open_debt_total,
        'open_receivable_total': open_receivable_total,
    }

    serializer = SummarySerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def category_breakdown_view(request):
    month, year = _get_month_and_year(request)
    user = request.user
    transaction_type = request.query_params.get('type', Transaction.TransactionType.EXPENSE)

    if transaction_type not in [
        Transaction.TransactionType.INCOME,
        Transaction.TransactionType.EXPENSE
    ]:
        return Response(
            {'detail': 'type must be INCOME or EXPENSE'},
            status=status.HTTP_400_BAD_REQUEST
        )

    qs = Transaction.objects.filter(
        user=user,
        transaction_type=transaction_type,
        transaction_date__year=year,
        transaction_date__month=month,
    ).values(
        'category_id',
        'category__name'
    ).annotate(
        total_amount=Sum('amount')
    ).order_by('-total_amount')

    grand_total = sum(item['total_amount'] for item in qs) if qs else Decimal('0.00')

    result = []
    for item in qs:
        total_amount = _decimal_or_zero(item['total_amount'])
        percentage = 0.0
        if grand_total > 0:
            percentage = round(float((total_amount / grand_total) * 100), 2)

        result.append({
            'category_id': item['category_id'],
            'category_name': item['category__name'],
            'total_amount': total_amount,
            'percentage': percentage,
        })

    serializer = CategoryBreakdownItemSerializer(result, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def income_vs_expense_trend_view(request):
    user = request.user
    group_by = request.query_params.get('group_by', 'day')
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')

    qs = Transaction.objects.filter(user=user)

    if date_from:
        qs = qs.filter(transaction_date__gte=date_from)
    if date_to:
        qs = qs.filter(transaction_date__lte=date_to)

    if group_by == 'day':
        trunc_expr = TruncDay('transaction_date')
        strftime_format = '%Y-%m-%d'
    elif group_by == 'week':
        trunc_expr = TruncWeek('transaction_date')
        strftime_format = '%Y-%m-%d'
    elif group_by == 'month':
        trunc_expr = TruncMonth('transaction_date')
        strftime_format = '%Y-%m'
    else:
        return Response(
            {'detail': 'group_by must be day, week, or month'},
            status=status.HTTP_400_BAD_REQUEST
        )

    grouped = qs.annotate(
        period_date=trunc_expr
    ).values(
        'period_date',
        'transaction_type'
    ).annotate(
        total_amount=Sum('amount')
    ).order_by('period_date')

    result_map = {}

    for row in grouped:
        period_date = row['period_date']
        period_key = period_date.strftime(strftime_format)

        if period_key not in result_map:
            result_map[period_key] = {
                'period': period_key,
                'income': Decimal('0.00'),
                'expense': Decimal('0.00'),
                'net': Decimal('0.00'),
            }

        if row['transaction_type'] == Transaction.TransactionType.INCOME:
            result_map[period_key]['income'] = _decimal_or_zero(row['total_amount'])
        else:
            result_map[period_key]['expense'] = _decimal_or_zero(row['total_amount'])

        result_map[period_key]['net'] = (
            result_map[period_key]['income'] -
            result_map[period_key]['expense']
        )

    result = list(result_map.values())
    serializer = TrendItemSerializer(result, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def calendar_view(request):
    month, year = _get_month_and_year(request)
    user = request.user

    grouped = Transaction.objects.filter(
        user=user,
        transaction_date__year=year,
        transaction_date__month=month,
    ).annotate(
        day=TruncDay('transaction_date')
    ).values(
        'day',
        'transaction_type'
    ).annotate(
        total_amount=Sum('amount')
    ).order_by('day')

    result_map = {}

    for row in grouped:
        day = row['day'].date()

        if day not in result_map:
            result_map[day] = {
                'date': day,
                'income': Decimal('0.00'),
                'expense': Decimal('0.00'),
                'net': Decimal('0.00'),
            }

        if row['transaction_type'] == Transaction.TransactionType.INCOME:
            result_map[day]['income'] = _decimal_or_zero(row['total_amount'])
        else:
            result_map[day]['expense'] = _decimal_or_zero(row['total_amount'])

        result_map[day]['net'] = (
            result_map[day]['income'] -
            result_map[day]['expense']
        )

    result = list(result_map.values())
    serializer = CalendarDaySerializer(result, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def budget_vs_actual_view(request):
    month, year = _get_month_and_year(request)
    user = request.user

    try:
        budget = Budget.objects.prefetch_related('limits').get(
            user=user,
            month=month,
            year=year
        )
    except Budget.DoesNotExist:
        return Response(
            {'detail': 'Budget not found for selected month/year.'},
            status=status.HTTP_404_NOT_FOUND
        )

    actual_income = Transaction.objects.filter(
        user=user,
        transaction_type=Transaction.TransactionType.INCOME,
        transaction_date__year=year,
        transaction_date__month=month,
    ).aggregate(total=Sum('amount'))['total']

    actual_expense = Transaction.objects.filter(
        user=user,
        transaction_type=Transaction.TransactionType.EXPENSE,
        transaction_date__year=year,
        transaction_date__month=month,
    ).aggregate(total=Sum('amount'))['total']

    total_expense_limit = budget.limits.aggregate(
        total=Sum('expense_limit')
    )['total']

    actual_income = _decimal_or_zero(actual_income)
    actual_expense = _decimal_or_zero(actual_expense)
    total_expense_limit = _decimal_or_zero(total_expense_limit)

    data = {
        'budget_id': budget.id,
        'month': budget.month,
        'year': budget.year,
        'planned_income': budget.planned_income,
        'actual_income': actual_income,
        'actual_expense': actual_expense,
        'total_expense_limit': total_expense_limit,
        'remaining_budget': total_expense_limit - actual_expense,
        'income_gap': actual_income - budget.planned_income,
    }

    serializer = BudgetVsActualSerializer(data)
    return Response(serializer.data, status=status.HTTP_200_OK)
from decimal import Decimal
from django.db.models import Sum, Q
from django.utils import timezone
from rest_framework import serializers

from categories.models import Category
from transactions.models import Transaction
from .models import Budget, BudgetCategoryLimit


class BudgetCategoryLimitSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    actual_expense = serializers.SerializerMethodField()
    usage_percent = serializers.SerializerMethodField()

    class Meta:
        model = BudgetCategoryLimit
        fields = [
            'id',
            'category',
            'category_name',
            'expense_limit',
            'actual_expense',
            'usage_percent',
            'created_at',
        ]

    def get_actual_expense(self, obj):
        total = Transaction.objects.filter(
            user=obj.budget.user,
            transaction_type=Transaction.TransactionType.EXPENSE,
            category=obj.category,
            transaction_date__year=obj.budget.year,
            transaction_date__month=obj.budget.month,
        ).aggregate(total=Sum('amount'))['total']

        return total or Decimal('0.00')

    def get_usage_percent(self, obj):
        actual = self.get_actual_expense(obj)
        if obj.expense_limit == 0:
            return 0
        return round((actual / obj.expense_limit) * 100, 2)


class BudgetCategoryLimitCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategoryLimit
        fields = [
            'id',
            'category',
            'expense_limit',
        ]
        read_only_fields = ['id']

    def validate_expense_limit(self, value):
        if value < 0:
            raise serializers.ValidationError('Expense limit cannot be negative.')
        return value

    def validate_category(self, value):
        request = self.context['request']
        if value.category_type != Category.CategoryType.EXPENSE:
            raise serializers.ValidationError('Only EXPENSE categories can be used in budget limits.')

        if not value.is_default and value.user_id != request.user.id:
            raise serializers.ValidationError('You can use only your own or default categories.')

        return value

    def create(self, validated_data):
        budget = self.context['budget']
        return BudgetCategoryLimit.objects.create(budget=budget, **validated_data)


class BudgetSerializer(serializers.ModelSerializer):
    limits = BudgetCategoryLimitSerializer(many=True, read_only=True)
    total_actual_expense = serializers.SerializerMethodField()
    total_limit = serializers.SerializerMethodField()
    remaining_budget = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = [
            'id',
            'month',
            'year',
            'planned_income',
            'total_actual_expense',
            'total_limit',
            'remaining_budget',
            'limits',
            'created_at',
            'updated_at',
        ]

    def get_total_actual_expense(self, obj):
        total = Transaction.objects.filter(
            user=obj.user,
            transaction_type=Transaction.TransactionType.EXPENSE,
            transaction_date__year=obj.year,
            transaction_date__month=obj.month,
        ).aggregate(total=Sum('amount'))['total']

        return total or Decimal('0.00')

    def get_total_limit(self, obj):
        total = obj.limits.aggregate(total=Sum('expense_limit'))['total']
        return total or Decimal('0.00')

    def get_remaining_budget(self, obj):
        total_limit = self.get_total_limit(obj)
        actual_expense = self.get_total_actual_expense(obj)
        return total_limit - actual_expense


class BudgetCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = [
            'id',
            'month',
            'year',
            'planned_income',
        ]
        read_only_fields = ['id']

    def validate_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError('Month must be between 1 and 12.')
        return value

    def validate_year(self, value):
        if value < 2000 or value > 2100:
            raise serializers.ValidationError('Year is out of allowed range.')
        return value

    def validate_planned_income(self, value):
        if value < 0:
            raise serializers.ValidationError('Planned income cannot be negative.')
        return value

    def validate(self, attrs):
        request = self.context['request']
        month = attrs.get('month', getattr(self.instance, 'month', None))
        year = attrs.get('year', getattr(self.instance, 'year', None))

        queryset = Budget.objects.filter(
            user=request.user,
            month=month,
            year=year
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError('Budget for this month and year already exists.')

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Budget.objects.create(user=user, **validated_data)
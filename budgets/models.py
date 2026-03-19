from decimal import Decimal
from django.conf import settings
from django.db import models

from categories.models import Category


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    planned_income = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-month', '-created_at']
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'month', 'year'],
                name='unique_budget_per_user_month_year'
            )
        ]

    def __str__(self):
        return f'{self.user.email} - {self.month}/{self.year}'


class BudgetCategoryLimit(models.Model):
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name='limits'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='budget_limits'
    )
    expense_limit = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category__name']
        verbose_name = 'Budget Category Limit'
        verbose_name_plural = 'Budget Category Limits'
        constraints = [
            models.UniqueConstraint(
                fields=['budget', 'category'],
                name='unique_budget_category_limit'
            )
        ]

    def __str__(self):
        return f'{self.budget} - {self.category.name}'
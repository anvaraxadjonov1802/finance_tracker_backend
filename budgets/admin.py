from django.contrib import admin
from .models import Budget, BudgetCategoryLimit


class BudgetCategoryLimitInline(admin.TabularInline):
    model = BudgetCategoryLimit
    extra = 0


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'month',
        'year',
        'planned_income',
        'created_at',
        'updated_at',
    )
    list_filter = ('year', 'month')
    search_fields = ('user__email', 'user__username')
    inlines = [BudgetCategoryLimitInline]


@admin.register(BudgetCategoryLimit)
class BudgetCategoryLimitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'budget',
        'category',
        'expense_limit',
        'created_at',
    )
    search_fields = ('budget__user__email', 'category__name')
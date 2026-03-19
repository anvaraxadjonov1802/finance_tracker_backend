from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'user',
        'account_type',
        'currency',
        'initial_balance',
        'current_balance',
        'is_active',
        'created_at',
    )
    list_filter = ('account_type', 'currency', 'is_active')
    search_fields = ('name', 'user__email', 'user__username')
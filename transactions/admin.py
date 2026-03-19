from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'transaction_type',
        'amount',
        'currency',
        'account',
        'category',
        'transaction_date',
        'created_at',
    )
    list_filter = ('transaction_type', 'currency', 'transaction_date')
    search_fields = (
        'description',
        'user__email',
        'account__name',
        'category__name',
    )
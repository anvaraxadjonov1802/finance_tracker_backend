from django.contrib import admin
from .models import Transfer


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'from_account',
        'to_account',
        'from_amount',
        'to_amount',
        'exchange_rate',
        'transfer_date',
        'created_at',
    )
    list_filter = ('from_currency', 'to_currency', 'transfer_date')
    search_fields = (
        'user__email',
        'from_account__name',
        'to_account__name',
        'note',
    )
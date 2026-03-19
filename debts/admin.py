from django.contrib import admin
from .models import DebtRecord


@admin.register(DebtRecord)
class DebtRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'person_name',
        'debt_type',
        'amount',
        'currency',
        'status',
        'due_date',
        'created_at',
        'closed_at',
    )
    list_filter = ('debt_type', 'status', 'currency', 'due_date')
    search_fields = (
        'person_name',
        'description',
        'user__email',
        'user__username',
    )
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone

from accounts.models import Account


class Transfer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transfers'
    )
    from_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='outgoing_transfers'
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='incoming_transfers'
    )

    from_amount = models.DecimalField(max_digits=14, decimal_places=2)
    to_amount = models.DecimalField(max_digits=14, decimal_places=2)

    from_currency = models.CharField(max_length=10)
    to_currency = models.CharField(max_length=10)

    exchange_rate = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        default=Decimal('1.000000')
    )

    note = models.CharField(max_length=255, blank=True, default='')
    transfer_date = models.DateField(default=timezone.localdate)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-transfer_date', '-created_at']
        verbose_name = 'Transfer'
        verbose_name_plural = 'Transfers'

    def __str__(self):
        return f'{self.from_account.name} -> {self.to_account.name}'
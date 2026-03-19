from decimal import Decimal
from django.conf import settings
from django.db import models


class Account(models.Model):
    class AccountType(models.TextChoices):
        CARD = 'CARD', 'Card'
        BANK_ACCOUNT = 'BANK_ACCOUNT', 'Bank Account'
        CASH = 'CASH', 'Cash'

    class Currency(models.TextChoices):
        UZS = 'UZS', 'Uzbek Som'
        USD = 'USD', 'US Dollar'
        EUR = 'EUR', 'Euro'
        RUB = 'RUB', 'Russian Ruble'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    name = models.CharField(max_length=100)
    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices
    )
    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.UZS
    )
    initial_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00')
    )
    current_balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00')
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def save(self, *args, **kwargs):
        if self._state.adding and self.current_balance == Decimal('0.00'):
            self.current_balance = self.initial_balance
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.currency})"
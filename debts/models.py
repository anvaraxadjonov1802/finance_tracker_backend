from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone


class DebtRecord(models.Model):
    class DebtType(models.TextChoices):
        DEBT = 'DEBT', 'Debt'
        RECEIVABLE = 'RECEIVABLE', 'Receivable'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        CLOSED = 'CLOSED', 'Closed'

    class Currency(models.TextChoices):
        UZS = 'UZS', 'Uzbek Som'
        USD = 'USD', 'US Dollar'
        EUR = 'EUR', 'Euro'
        RUB = 'RUB', 'Russian Ruble'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='debts'
    )

    debt_type = models.CharField(
        max_length=20,
        choices=DebtType.choices
    )
    person_name = models.CharField(max_length=120)
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00')
    )
    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.UZS
    )
    description = models.CharField(max_length=255, blank=True, default='')
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['status', '-created_at']
        verbose_name = 'Debt Record'
        verbose_name_plural = 'Debt Records'

    def mark_closed(self):
        self.status = self.Status.CLOSED
        self.closed_at = timezone.now()
        self.save(update_fields=['status', 'closed_at', 'updated_at'])

    def reopen(self):
        self.status = self.Status.OPEN
        self.closed_at = None
        self.save(update_fields=['status', 'closed_at', 'updated_at'])

    def __str__(self):
        return f'{self.person_name} - {self.debt_type} - {self.amount} {self.currency}'
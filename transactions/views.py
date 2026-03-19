from django.db import transaction as db_transaction
from rest_framework import generics, permissions

from accounts.models import Account
from .models import Transaction
from .serializers import TransactionReadSerializer, TransactionWriteSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(
            user=self.request.user
        ).select_related('account', 'category')

        transaction_type = self.request.query_params.get('type')
        account_id = self.request.query_params.get('account')
        category_id = self.request.query_params.get('category')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        if account_id:
            queryset = queryset.filter(account_id=account_id)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if date_from:
            queryset = queryset.filter(transaction_date__gte=date_from)

        if date_to:
            queryset = queryset.filter(transaction_date__lte=date_to)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransactionWriteSerializer
        return TransactionReadSerializer


class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user
        ).select_related('account', 'category')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TransactionWriteSerializer
        return TransactionReadSerializer

    def perform_destroy(self, instance):
        with db_transaction.atomic():
            account = Account.objects.select_for_update().get(
                id=instance.account_id,
                user=self.request.user
            )

            if instance.transaction_type == Transaction.TransactionType.INCOME:
                account.current_balance -= instance.amount
            else:
                account.current_balance += instance.amount

            account.save()
            instance.delete()
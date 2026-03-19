from django.db import transaction as db_transaction
from rest_framework import generics, permissions

from accounts.models import Account
from .models import Transfer
from .serializers import TransferReadSerializer, TransferWriteSerializer


class TransferListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Transfer.objects.filter(
            user=self.request.user
        ).select_related('from_account', 'to_account')

        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        from_account = self.request.query_params.get('from_account')
        to_account = self.request.query_params.get('to_account')

        if date_from:
            queryset = queryset.filter(transfer_date__gte=date_from)

        if date_to:
            queryset = queryset.filter(transfer_date__lte=date_to)

        if from_account:
            queryset = queryset.filter(from_account_id=from_account)

        if to_account:
            queryset = queryset.filter(to_account_id=to_account)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransferWriteSerializer
        return TransferReadSerializer


class TransferRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transfer.objects.filter(
            user=self.request.user
        ).select_related('from_account', 'to_account')

    serializer_class = TransferReadSerializer

    def perform_destroy(self, instance):
        with db_transaction.atomic():
            locked_accounts = {
                account.id: account
                for account in Account.objects.select_for_update().filter(
                    id__in=sorted([instance.from_account_id, instance.to_account_id]),
                    user=self.request.user
                )
            }

            from_account = locked_accounts[instance.from_account_id]
            to_account = locked_accounts[instance.to_account_id]

            # rollback
            from_account.current_balance += instance.from_amount
            to_account.current_balance -= instance.to_amount

            from_account.save()
            to_account.save()

            instance.delete()
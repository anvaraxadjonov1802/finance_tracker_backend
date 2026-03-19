from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction as db_transaction
from rest_framework import serializers

from accounts.models import Account
from .models import Transfer


class TransferReadSerializer(serializers.ModelSerializer):
    from_account_name = serializers.CharField(source='from_account.name', read_only=True)
    to_account_name = serializers.CharField(source='to_account.name', read_only=True)

    class Meta:
        model = Transfer
        fields = [
            'id',
            'from_account',
            'from_account_name',
            'to_account',
            'to_account_name',
            'from_amount',
            'to_amount',
            'from_currency',
            'to_currency',
            'exchange_rate',
            'note',
            'transfer_date',
            'created_at',
        ]


class TransferWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = [
            'id',
            'from_account',
            'to_account',
            'from_amount',
            'exchange_rate',
            'note',
            'transfer_date',
        ]
        read_only_fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            self.fields['from_account'].queryset = Account.objects.filter(
                user=request.user,
                is_active=True
            )
            self.fields['to_account'].queryset = Account.objects.filter(
                user=request.user,
                is_active=True
            )

    def validate_from_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Transfer amount must be greater than 0.')
        return value

    def validate_exchange_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError('Exchange rate must be greater than 0.')
        return value

    def validate(self, attrs):
        from_account = attrs.get('from_account')
        to_account = attrs.get('to_account')

        if from_account == to_account:
            raise serializers.ValidationError({
                'to_account': 'From account and To account must be different.'
            })

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user

        from_account_id = validated_data['from_account'].id
        to_account_id = validated_data['to_account'].id

        with db_transaction.atomic():
            locked_accounts = {
                account.id: account
                for account in Account.objects.select_for_update().filter(
                    id__in=sorted([from_account_id, to_account_id]),
                    user=user
                )
            }

            from_account = locked_accounts[from_account_id]
            to_account = locked_accounts[to_account_id]

            from_amount = validated_data['from_amount']
            exchange_rate = validated_data.get('exchange_rate', Decimal('1.000000'))

            if from_account.currency == to_account.currency:
                exchange_rate = Decimal('1.000000')
                to_amount = from_amount
            else:
                to_amount = (from_amount * exchange_rate).quantize(
                    Decimal('0.01'),
                    rounding=ROUND_HALF_UP
                )

            from_account.current_balance -= from_amount
            to_account.current_balance += to_amount

            from_account.save()
            to_account.save()

            return Transfer.objects.create(
                user=user,
                from_account=from_account,
                to_account=to_account,
                from_amount=from_amount,
                to_amount=to_amount,
                from_currency=from_account.currency,
                to_currency=to_account.currency,
                exchange_rate=exchange_rate,
                note=validated_data.get('note', ''),
                transfer_date=validated_data.get('transfer_date'),
            )
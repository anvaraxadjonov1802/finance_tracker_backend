from django.db import transaction as db_transaction
from rest_framework import serializers

from accounts.models import Account
from categories.models import Category
from .models import Transaction


class TransactionReadSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source='account.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'account',
            'account_name',
            'category',
            'category_name',
            'transaction_type',
            'amount',
            'currency',
            'description',
            'transaction_date',
            'created_at',
            'updated_at',
        ]


class TransactionWriteSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Transaction
        fields = [
            'id',
            'account',
            'category',
            'transaction_type',
            'amount',
            'description',
            'transaction_date',
        ]
        read_only_fields = ['id']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than 0.')
        return value

    def validate_account(self, value):
        user = self.context['request'].user
        if value.user_id != user.id:
            raise serializers.ValidationError("You can use only your own account.")
        if not value.is_active:
            raise serializers.ValidationError("Inactive account cannot be used.")
        return value

    def validate_category(self, value):
        user = self.context['request'].user
        if not value.is_default and value.user_id != user.id:
            raise serializers.ValidationError("You can use only your own or default categories.")
        return value

    def validate(self, attrs):
        transaction_type = attrs.get('transaction_type') or getattr(self.instance, 'transaction_type', None)
        category = attrs.get('category') or getattr(self.instance, 'category', None)

        if category and transaction_type and category.category_type != transaction_type:
            raise serializers.ValidationError({
                'category': 'Category type must match transaction type.'
            })

        return attrs

    def _apply_effect(self, account, transaction_type, amount):
        if transaction_type == Transaction.TransactionType.INCOME:
            account.current_balance += amount
        else:
            account.current_balance -= amount

    def _rollback_effect(self, account, transaction_type, amount):
        if transaction_type == Transaction.TransactionType.INCOME:
            account.current_balance -= amount
        else:
            account.current_balance += amount

    def create(self, validated_data):
        user = self.context['request'].user

        with db_transaction.atomic():
            account = Account.objects.select_for_update().get(
                pk=validated_data['account'].pk,
                user=user
            )

            self._apply_effect(
                account=account,
                transaction_type=validated_data['transaction_type'],
                amount=validated_data['amount']
            )
            account.save()

            validated_data['user'] = user
            validated_data['account'] = account
            validated_data['currency'] = account.currency

            return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user

        new_account_id = validated_data.get('account', instance.account).id
        involved_account_ids = sorted({instance.account_id, new_account_id})

        with db_transaction.atomic():
            locked_accounts = {
                account.id: account
                for account in Account.objects.select_for_update().filter(
                    id__in=involved_account_ids,
                    user=user
                )
            }

            old_account = locked_accounts[instance.account_id]
            new_account = locked_accounts[new_account_id]

            self._rollback_effect(
                account=old_account,
                transaction_type=instance.transaction_type,
                amount=instance.amount
            )

            new_transaction_type = validated_data.get('transaction_type', instance.transaction_type)
            new_amount = validated_data.get('amount', instance.amount)

            self._apply_effect(
                account=new_account,
                transaction_type=new_transaction_type,
                amount=new_amount
            )

            old_account.save()
            if new_account.id != old_account.id:
                new_account.save()

            instance.account = new_account
            instance.category = validated_data.get('category', instance.category)
            instance.transaction_type = new_transaction_type
            instance.amount = new_amount
            instance.currency = new_account.currency
            instance.description = validated_data.get('description', instance.description)
            instance.transaction_date = validated_data.get('transaction_date', instance.transaction_date)
            instance.save()

            return instance
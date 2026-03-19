from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'name',
            'account_type',
            'currency',
            'initial_balance',
            'current_balance',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'current_balance', 'created_at', 'updated_at']


class AccountCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'name',
            'account_type',
            'currency',
            'initial_balance',
            'is_active',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        return Account.objects.create(user=user, **validated_data)
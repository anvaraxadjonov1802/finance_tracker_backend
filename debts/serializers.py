from rest_framework import serializers
from .models import DebtRecord


class DebtRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtRecord
        fields = [
            'id',
            'debt_type',
            'person_name',
            'amount',
            'currency',
            'description',
            'due_date',
            'status',
            'created_at',
            'updated_at',
            'closed_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'closed_at']


class DebtRecordCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtRecord
        fields = [
            'id',
            'debt_type',
            'person_name',
            'amount',
            'currency',
            'description',
            'due_date',
            'status',
        ]
        read_only_fields = ['id']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than 0.')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        return DebtRecord.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get('status', instance.status)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if old_status != new_status:
            if new_status == DebtRecord.Status.CLOSED:
                from django.utils import timezone
                instance.closed_at = timezone.now()
            elif new_status == DebtRecord.Status.OPEN:
                instance.closed_at = None

        instance.save()
        return instance
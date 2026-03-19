from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'category_type',
            'icon',
            'color',
            'is_default',
            'created_at',
        ]
        read_only_fields = ['id', 'is_default', 'created_at']


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'category_type',
            'icon',
            'color',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        return Category.objects.create(user=user, is_default=False, **validated_data)
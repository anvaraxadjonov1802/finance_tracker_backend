from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Budget, BudgetCategoryLimit
from .serializers import (
    BudgetSerializer,
    BudgetCreateUpdateSerializer,
    BudgetCategoryLimitSerializer,
    BudgetCategoryLimitCreateUpdateSerializer,
)


class BudgetListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Budget.objects.filter(user=self.request.user).prefetch_related('limits__category')

        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        if month:
            queryset = queryset.filter(month=month)

        if year:
            queryset = queryset.filter(year=year)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BudgetCreateUpdateSerializer
        return BudgetSerializer


class BudgetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).prefetch_related('limits__category')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BudgetCreateUpdateSerializer
        return BudgetSerializer


class BudgetLimitListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_budget(self):
        return Budget.objects.get(pk=self.kwargs['budget_id'], user=self.request.user)

    def get_queryset(self):
        budget = self.get_budget()
        return BudgetCategoryLimit.objects.filter(budget=budget).select_related('category', 'budget')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BudgetCategoryLimitCreateUpdateSerializer
        return BudgetCategoryLimitSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['budget'] = self.get_budget()
        return context


class BudgetLimitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_budget(self):
        return Budget.objects.get(pk=self.kwargs['budget_id'], user=self.request.user)

    def get_queryset(self):
        budget = self.get_budget()
        return BudgetCategoryLimit.objects.filter(
            budget=budget
        ).select_related('category', 'budget')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BudgetCategoryLimitCreateUpdateSerializer
        return BudgetCategoryLimitSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['budget'] = self.get_budget()
        return context


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_budget_view(request):
    today = timezone.localdate()
    month = request.query_params.get('month', today.month)
    year = request.query_params.get('year', today.year)

    try:
        budget = Budget.objects.prefetch_related('limits__category').get(
            user=request.user,
            month=month,
            year=year
        )
    except Budget.DoesNotExist:
        return Response(
            {'detail': 'Budget not found for selected month/year.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = BudgetSerializer(budget)
    return Response(serializer.data, status=status.HTTP_200_OK)
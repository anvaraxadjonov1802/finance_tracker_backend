from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import DebtRecord
from .serializers import DebtRecordSerializer, DebtRecordCreateUpdateSerializer


class DebtRecordListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = DebtRecord.objects.filter(user=self.request.user)

        debt_type = self.request.query_params.get('type')
        record_status = self.request.query_params.get('status')
        currency = self.request.query_params.get('currency')
        person_name = self.request.query_params.get('person_name')

        if debt_type:
            queryset = queryset.filter(debt_type=debt_type)

        if record_status:
            queryset = queryset.filter(status=record_status)

        if currency:
            queryset = queryset.filter(currency=currency)

        if person_name:
            queryset = queryset.filter(person_name__icontains=person_name)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DebtRecordCreateUpdateSerializer
        return DebtRecordSerializer


class DebtRecordRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DebtRecord.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return DebtRecordCreateUpdateSerializer
        return DebtRecordSerializer


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def close_debt_record(request, pk):
    try:
        debt_record = DebtRecord.objects.get(pk=pk, user=request.user)
    except DebtRecord.DoesNotExist:
        return Response(
            {'detail': 'Debt record not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    debt_record.mark_closed()
    serializer = DebtRecordSerializer(debt_record)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def reopen_debt_record(request, pk):
    try:
        debt_record = DebtRecord.objects.get(pk=pk, user=request.user)
    except DebtRecord.DoesNotExist:
        return Response(
            {'detail': 'Debt record not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    debt_record.reopen()
    serializer = DebtRecordSerializer(debt_record)
    return Response(serializer.data, status=status.HTTP_200_OK)
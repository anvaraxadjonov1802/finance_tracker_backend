from django.urls import path
from .views import TransactionListCreateView, TransactionRetrieveUpdateDestroyView

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
]
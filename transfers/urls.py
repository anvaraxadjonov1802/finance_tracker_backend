from django.urls import path
from .views import TransferListCreateView, TransferRetrieveDestroyView

urlpatterns = [
    path('', TransferListCreateView.as_view(), name='transfer-list-create'),
    path('<int:pk>/', TransferRetrieveDestroyView.as_view(), name='transfer-detail'),
]
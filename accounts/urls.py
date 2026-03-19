from django.urls import path
from .views import AccountListCreateView, AccountRetrieveUpdateDestroyView

urlpatterns = [
    path('', AccountListCreateView.as_view(), name='account-list-create'),
    path('<int:pk>/', AccountRetrieveUpdateDestroyView.as_view(), name='account-detail'),
]
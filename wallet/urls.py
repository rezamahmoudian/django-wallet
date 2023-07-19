from .views import WalletListView, TransactionView, WalletDetailView
from django.urls import path, include

app_name = 'wallet'

urlpatterns = [
    path('wallets/', WalletListView.as_view(), name='wallet'),
    path('wallets/<int:pk>', WalletDetailView.as_view(), name='wallet-detail'),
    path('transaction/', TransactionView.as_view(), name='wallet'),
]

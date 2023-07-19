from .views import WalletListView, TransactionView, WalletDetailView, TransactionDetailView
from django.urls import path, include

app_name = 'wallet'

urlpatterns = [
    path('wallets/', WalletListView.as_view(), name='wallet'),
    path('wallet-detail/', WalletDetailView.as_view(), name='wallet-detail'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
    path('transaction-detail/', TransactionDetailView.as_view(), name='transaction-detail'),
]

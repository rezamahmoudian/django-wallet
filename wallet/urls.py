from .views import WalletListView, TransactionView
from django.urls import path, include

app_name = 'wallet'

urlpatterns = [
    path('wallets/', WalletListView.as_view(), name='wallet'),
    path('transaction/', TransactionView.as_view(), name='wallet')

]

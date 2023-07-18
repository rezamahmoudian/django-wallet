from django.shortcuts import render
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .models import Wallet, Transaction
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView

# Create your views here.


class WalletListView(ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class TransactionView(APIView):
    def get(self, request, format=None):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        print(request.data['wallet'])
        if serializer.is_valid():
            serializer.save()
            wallet = Wallet.objects.get(id=request.data["wallet"])
            wallet.balance += request.data["amount"]
            wallet.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

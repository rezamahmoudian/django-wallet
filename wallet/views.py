from django.shortcuts import render
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .models import Wallet, Transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView

# Create your views here.


class WalletListView(ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class WalletDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj = Wallet.objects.get(user_id=request.user.id)
        serializer = WalletSerializer(obj)

        return Response(serializer.data)
    # queryset = Wallet.objects.get(user=get_user_model())


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
            wallet.balance += int(request.data["amount"])
            wallet.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):
    def get(self, request):
        wallet = Wallet.objects.get(user_id=request.user.id)
        transactions = Transaction.objects.get(wallet_id=wallet.id)
        print(transactions)
        serializer = TransactionSerializer(transactions)
        return Response(serializer.data)

    # گرفتن آیدی کیف پول از api ورودی

    # def post(self, request):
    #     serializer = TransactionSerializer(data=request.data)
    #     print(request.data['wallet'])
    #     if serializer.is_valid():
    #         print(serializer.data)
    #         # serializer.save()
    #         wallet = Wallet.objects.get(id=request.data["wallet"])
    #         wallet.balance += int(request.data["amount"])
    #         wallet.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# اضافه کردن آیدی کیف پول بصورت اتوماتیک (از api نمیگیره)
    def post(self, request):
        data = request.data
        data = dict(data)
        print(data)
        data['wallet'] = Wallet.objects.get(user_id=request.user.id).id
        print("data2")
        print(data)
        data = request.data
        serializer = TransactionSerializer(data=request.data)
        # print(serializer.data)
        if serializer.is_valid():
            serializer.save()
            wallet = Wallet.objects.get(id=request.data["wallet"])
            wallet.balance += int(request.data["amount"])
            wallet.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer, ShabaSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .models import Wallet, Transaction, Shaba
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from django.core.management.utils import get_random_secret_key
from django.http import QueryDict
from django.core.cache import cache

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
    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
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
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            wallet = Wallet.objects.get(id=request.data["wallet"])
            wallet.balance += int(request.data["amount"])
            wallet.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# shaba ra bsazad vali ba verify false, va activate code ra b user bdahad
class CreateShabaView(APIView):
    def post(self, request):
        serializer = ShabaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            print("serializer is valid")
            serializer.save()
        return Response(serializer.data)


# agar user active link ra bzanad in view farakhani shavad va verify ra True konad
class ActivateShabaView(APIView):
    def get(self, request, active_link):
        print("activate key = " + active_link)
        active_key = cache.get('active_link')
        print("active cache")
        print(active_key)
        if active_link==active_key:
            print("its ok")
        shaba = Shaba.objects.get(active_link=active_link)
        print(shaba)
        return Response()




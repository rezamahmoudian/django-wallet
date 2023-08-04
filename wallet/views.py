from django.shortcuts import render
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer, ShabaSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .models import Wallet, Transaction, Shaba
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.generics import CreateAPIView, ListCreateAPIView
from django.core.cache import cache
from django.urls import reverse
import random
import string

# Create your views here.


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str


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
        transactions = Transaction.objects.filter(wallet_id=wallet.id)
        print(transactions)
        serializer = TransactionSerializer(data=transactions)
        serializer.is_valid()
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
        data['wallet'] = request.user.wallet.id-0
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #####################################################################
            wallet = Wallet.objects.get(id=request.data["wallet"])
            wallet.balance += int(request.data["amount"])
            wallet.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# shaba ra bsazad vali ba verify false, va activate code ra b user bdahad
class CreateShabaView(APIView):
    def post(self, request):
        data = request.data
        serializer = ShabaSerializer(data=data, context={'request': request})

        shaba_number = data['shaba_number']
        bank_name = data["bank_name"]
        full_name = data["full_name"]

        active_key = get_random_string(72)

        if serializer.is_valid():
            print("serializer is valid")
            cache.set("shaba_data", {
                "shaba_number": shaba_number,
                "bank_name": bank_name,
                "full_name": full_name,
                "active_key": active_key,
                "wallet_id": request.user.wallet.id
            }, 180)

            active_link = reverse('wallet:shaba_active', kwargs={'active_key': active_key})
            print(active_link)
            print("active link")
            print(active_link)
            return Response({
                "shaba_data": serializer.data,
                "activelink": active_link
            })
        else:
            return Response({
                "message": "your data is not valid"
            })


# agar user active link ra bzanad in view farakhani shavad va verify ra True konad
class ActivateShabaView(APIView):
    def get(self, request, active_key):

        shaba_data = cache.get('shaba_data')
        if shaba_data is not None:
            print(shaba_data)
            if active_key == shaba_data["active_key"]:
                print("its ok")
                try:
                    shaba = Shaba.objects.create(verified=True, **shaba_data)
                    shaba.save()
                    return Response({
                        "message": "shomare shaba active shod"
                    })
                except:
                    return Response({
                        "message": "shomare shaba shoma active ast"
                    })
            else:
                return Response({
                    "message": "active link is not correct"
                })
        else:
            return Response({
                "message": "shomare shaba active nashod!!!"
            })

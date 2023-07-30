from .models import Wallet, Transaction, Shaba
from rest_framework import serializers
from django.core.management.utils import get_random_secret_key
from django.core.cache import cache
import random
import string


def get_random_string(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class ShabaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shaba
        fields = ['shaba_number', 'bank_name', 'full_name']

    def create(self, validated_data):
        request = self.context.get("request")
        active_link = get_random_string(72)
        wallet_id = request.user.wallet.id
        wallet = Wallet.objects.get(id=wallet_id)
        print("validation data: ")
        print(validated_data)
        shaba = Shaba.objects.create(active_link=active_link, wallet=wallet, **validated_data)
        cache.set('active_link', active_link, 5000)
        return shaba

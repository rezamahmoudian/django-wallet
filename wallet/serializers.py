from .models import Wallet, Transaction, Shaba
from rest_framework import serializers
from django.core.management.utils import get_random_secret_key
import json


class WalletSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wallet
		fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = "__all__"


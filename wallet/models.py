from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Wallet(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)

    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='wallet', on_delete=models.PROTECT, default='')
    transaction_id = models.AutoField(primary_key=True)
    amount = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "معامله"
        verbose_name_plural = "معاملات"


class Shaba(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    shaba_number = models.CharField(max_length=24, unique=True)
    bank_name = models.CharField(max_length=24)
    full_name = models.CharField(max_length=24)
    active_link = models.CharField(max_length=128, verbose_name="لینک ارسال شده", unique=True)
    verified = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "shaba"
        verbose_name_plural = "shaba"


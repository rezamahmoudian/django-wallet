from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Wallet(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)

    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    amount = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    wallet = models.ForeignKey(Wallet, related_name='wallet', on_delete=models.PROTECT, default='')

    class Meta:
        verbose_name = "معامله"
        verbose_name_plural = "معاملات"


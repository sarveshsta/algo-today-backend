import uuid

from django.contrib.auth.models import (AbstractBaseUser, AbstractUser, Group,
                                        Permission, PermissionsMixin)
from django.db import models

# Create your models here.


class Timestamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractBaseUser, PermissionsMixin, Timestamps):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False, blank=False, default="")
    phone = models.CharField(max_length=50, null=False, blank=False, unique=True, default="", db_index=True)
    email = models.EmailField(null=False, blank=False, unique=True, default="")
    username = models.CharField(null=True, blank=True, default=None, max_length=20)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['phone', 'email', 'name']
    def __str__(self):
        if self.phone:
            return self.phone
        elif self.email:
            return self.email
        return f"{self.name} - {self.phone} - {self.email}"
    
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='custom_user_set')

class PhoneOTP(Timestamps):
    phone = models.IntegerField(null=False, blank=False, unique=True, default="", db_index=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)


class Wallet(Timestamps):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name='User-Wallet', blank=True, 
                            related_name='user_wallet', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class Strategy(Timestamps):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, null=True, blank=True, default="")
    strategy_id = models.CharField(max_length=40, default=None, blank=True, null=True)
    description = models.TextField()
    user = models.ForeignKey(User, verbose_name='User-Strategy', blank=True, 
                            on_delete=models.CASCADE, related_name='algotrade_user_strategy')
    advantages = models.TextField()
    

class UserTradeDetails(Timestamps):
    TRADE_CHOICES = (
    ("SELL", "SELL"),
    ("BUY", "BUY"))
    CEPE = (
    ("CALL", "CALL"),
    ("PUT", "PUT"))


    user = models.ForeignKey(User, verbose_name='User-Trades', blank=True, 
                            related_name='user_trades', on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=10, default=None, null=True, choices=TRADE_CHOICES)
    cepe = models.CharField(max_length=10, default=None, null=True, choices=TRADE_CHOICES)
    trade_price = models.CharField(max_length=10, default="0", null=True)
    index = models.CharField(max_length=25, default=None, null=True)
    token = models.IntegerField(default=0)
    symbol = models.CharField(max_length=40, default=None, null=True)
    
    

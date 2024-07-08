import uuid
from django.db import models
from users.models import Timestamps, User

# Create your models here.

class UserStrategy(Timestamps):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, null=True, blank=True, default="")
    strategy_id = models.CharField(max_length=40, default=None, blank=True, null=True)
    description = models.TextField()
    user = models.ForeignKey(User, verbose_name='User-Strategy', blank=True, 
                            on_delete=models.CASCADE, related_name='user_strategy')
    advantages = models.TextField()

class UserOrders(Timestamps):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, verbose_name='User-Order', blank=True, 
                            on_delete=models.CASCADE, related_name='user_order')

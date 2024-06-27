from django.contrib import admin
from .models import UserOrders, UserStrategy

# Register your models here.
admin.site.register(UserStrategy)
admin.site.register(UserOrders)
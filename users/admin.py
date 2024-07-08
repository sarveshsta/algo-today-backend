from django.contrib import admin
from .models import PhoneOTP, User, Wallet

# Register your models here.
class AlgoUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone')

class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp', 'is_verified')

class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount')

class StrategyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'strategy_id')

admin.site.register(User, AlgoUserAdmin)
admin.site.register(PhoneOTP, PhoneOTPAdmin)
admin.site.register(Wallet, WalletAdmin)
# admin.site.register(Strategy, StrategyAdmin)


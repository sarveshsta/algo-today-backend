from django.contrib import admin

from .models import PhoneOTP, User

# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'email', 'phone')

class PhoneOTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp', 'is_verified')
# admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP, PhoneOTPAdmin)


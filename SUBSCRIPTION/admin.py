from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, PaymentHistory

@admin.register(SubscriptionPlan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_months', 'is_active')

@admin.register(UserSubscription)
class UserSubAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'end_date')
    list_filter = ('status', 'plan')

@admin.register(PaymentHistory)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at')

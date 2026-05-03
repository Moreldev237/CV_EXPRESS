from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription, PaymentHistory


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    is_free = serializers.BooleanField( read_only=True)
    interval_display = serializers.CharField(read_only=True)

    class Meta:
        model = SubscriptionPlan
        fields = [
            'id',
            'name',
            'description',
            'price',
            'duration_months',
            'interval',
            'interval_display',
            'features',
            'stripe_price_id',
            'is_active',
            'is_featured',
            'order',
            'is_free',
        ]
        read_only_fields = ['id', 'is_free', 'interval_display']


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan_details = SubscriptionPlanSerializer(source='plan', read_only=True)
    remaining_days = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'plan',
            'plan_details',
            'status',
            'start_date',
            'end_date',
            'remaining_days',
            'stripe_subscription_id',
        ]
        read_only_fields = ['id', 'start_date', 'remaining_days', 'stripe_subscription_id']


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = '__all__'


class SubscribeRequestSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    payment_method_id = serializers.CharField(required=False)

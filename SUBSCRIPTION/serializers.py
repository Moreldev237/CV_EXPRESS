from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription, PaymentHistory

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan_details = SubscriptionPlanSerializer(source='plan', read_only=True)
    
    class Meta:
        model = UserSubscription
        fields = ['id', 'plan', 'plan_details', 'status', 'start_date', 'end_date']
        read_only_fields = ['id', 'start_date']

class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = '__all__'

class SubscribeRequestSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    payment_method_id = serializers.CharField(required=False)
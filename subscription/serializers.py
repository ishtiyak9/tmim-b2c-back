from rest_framework import serializers

from subscription.models import Subscription, SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription

        fields = ['id', 'fees', 'payment_type', 'payment_status', 'vendor', 'subscription_plan', 'start_date',
                  'end_date', 'created_by', 'updated_by', 'is_deleted', 'paytab_data']

    def create(self, vailidated_data):
        subscription_plan = vailidated_data.get('subscription_plan')
        subscription_plan_details = SubscriptionPlan.objects.get(pk=subscription_plan.id)

        fees = vailidated_data.get('fees')
        payment_status = False
        if fees == subscription_plan_details.fees:
            payment_status = True

        subscription = Subscription.objects.create(**vailidated_data, payment_status=payment_status)

        return subscription

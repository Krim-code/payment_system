from rest_framework import serializers
from .models import Payment, Organization

class PaymentWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['operation_id', 'amount', 'payer_inn', 'document_number', 'document_date']

class OrganizationBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['inn', 'balance']


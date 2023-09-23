from rest_framework import serializers
from Main.models import Operations_account

class OperationsAccountSerializer(serializers.ModelSerializer):
    total_amount_available = serializers.SerializerMethodField()

    class Meta:
        model = Operations_account
        fields = ('total_amount_available', 'amount_available_cash', 'amount_available_transfer')

    def get_total_amount_available(self, obj):
        return obj.get_total_amount_available()

from rest_framework import serializers
from Main.models import *

class OperationsAccountSerializer(serializers.ModelSerializer):
    total_amount_available = serializers.SerializerMethodField()

    class Meta:
        model = Operations_account
        fields = ('total_amount_available', 'amount_available_cash', 'amount_available_transfer')

    def get_total_amount_available(self, obj):
        return obj.get_total_amount_available()


class SummaryTransactionSerializer(serializers.Serializer):
    date = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class CashandTransactionTotalSerializer (serializers.Serializer):
    cash_total =  serializers.IntegerField()
    transfer_total = serializers.IntegerField()


class OperationsAccountCashTransactionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operations_account_transaction_record
        fields = ('time', 'amount', 'transaction_category', 'particulars', 'name_of_reciever', 'is_approved' )


class CashTransactionReadSerializer (serializers.ModelSerializer):
    class Meta:
        model = Operations_account_transaction_record
        fields = ('time', 'amount', 'transaction_category', 'particulars', 'name_of_reciever', 'is_approved' )

class CashTransactionWriteSerializer (serializers.ModelSerializer):
    class Meta:
        model = Operations_account_transaction_record
        fields = ('time', 'amount', 'transaction_category', 'particulars', 'name_of_reciever', 'is_approved' )
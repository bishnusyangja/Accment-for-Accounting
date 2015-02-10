from rest_framework import serializers

from bank.models import BankDeposit, BankDepositRow, BankPayment, BankPaymentRow


class BankDepositRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDepositRow


class BankDepositSerializer(serializers.ModelSerializer):
    rows = BankDepositRowSerializer()

    class Meta:
        model = BankDeposit


class BankPaymentRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankPaymentRow


class BankPaymentSerializer(serializers.ModelSerializer):
    rows = BankPaymentRowSerializer()

    class Meta:
        model = BankPayment

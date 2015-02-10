from datetime import date, datetime
from rest_framework import serializers
from models import Account, Category, Party, TaxScheme, InterestScheme, BankAccountDetail, AccountTaxDetail, PartyAccountDetail
from types import *


class TaxSchemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaxScheme


class InterestSchemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterestScheme


class BankAccountDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccountDetail


class PartyAccountDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartyAccountDetail


class AccountTaxDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountTaxDetail


class AccountSerializer(serializers.ModelSerializer):
    opening = serializers.SerializerMethodField('get_last_day_closing')
    categories = serializers.Field()
    pri_tax = serializers.Field(source='get_pri_tax')
    sec_tax = serializers.Field(source='get_sec_tax')
    tax_detail = AccountTaxDetailSerializer()
    party_detail = PartyAccountDetailSerializer()
    bank_detail = BankAccountDetailSerializer()

    class Meta:
        model = Account
        exclude = ['code', 'company', 'opening_as_on_date']

    def __init__(self, *args, **kwargs):
        day = kwargs.pop('day', None)
        super(AccountSerializer, self).__init__(*args, **kwargs)
        if day is not None:
            if type(day) is UnicodeType:
                self.day = datetime.strptime(day, '%Y-%m-%d').date()
            else:
                self.day = day
        else:
            self.day = date.today()

    def get_last_day_closing(self, obj):
        return obj.get_day_opening(self.day)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['company', 'description', 'is_default']


class PartySerializer(serializers.ModelSerializer):
    customer_balance = serializers.Field(source='customer_account.get_balance')
    supplier_balance = serializers.Field(source='supplier_account.get_balance')

    class Meta:
        model = Party


class CashVendorSerializer(serializers.ModelSerializer):
    category = serializers.Field(source='category.name')
    address = serializers.SerializerMethodField('get_address')
    categories = serializers.Field()

    def get_address(self, obj):
        if obj.category.name == 'Suppliers':
            return obj.supplier_detail.address
        return None

    class Meta:
        model = Account
        fields = ['id', 'name', 'category', 'address', 'categories']

from datetime import date

from rest_framework import serializers

from models import Item, InventoryAccount, Category, PhysicalStockRow, PhysicalStockVoucher


class PhysicalStockRowSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item_id')

    class Meta:
        model = PhysicalStockRow
        exclude = ['item']


class PhysicalStockVoucherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    particulars = PhysicalStockRowSerializer()

    class Meta:
        model = PhysicalStockVoucher
        exclude = ['company']


class InventoryAccountSerializer(serializers.ModelSerializer):
    opening = serializers.SerializerMethodField('get_last_day_closing')
    rate = serializers.SerializerMethodField('get_rate')
    category = serializers.Field(source='get_category')
    unit = serializers.Field(source='get_unit')

    class Meta:
        model = InventoryAccount
        fields = ['id', 'name', 'company']

    def __init__(self, *args, **kwargs):
        day = kwargs.pop('day', None)
        super(InventoryAccountSerializer, self).__init__(*args, **kwargs)
        if day is not None:
            self.day = day
        else:
            self.day = date.today()

    def get_last_day_closing(self, obj):
        return obj.get_day_opening(self.day)

    def get_rate(self, obj):
        return 0


class ItemSerializer(serializers.ModelSerializer):
    unit = serializers.Field(source='get_unit')
    opening = serializers.SerializerMethodField('get_last_day_closing')

    class Meta:
        model = Item

    def __init__(self, *args, **kwargs):
        day = kwargs.pop('day', None)
        super(ItemSerializer, self).__init__(*args, **kwargs)
        if day is not None:
            self.day = day
        else:
            self.day = date.today()

    def get_last_day_closing(self, obj):
        return obj.get_current_stock(self.day)


class InventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

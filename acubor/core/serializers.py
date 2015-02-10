from rest_framework import serializers

from ledger.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

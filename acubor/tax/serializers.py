from rest_framework import serializers

from models import TaxScheme


class TaxSchemeSerializer(serializers.ModelSerializer):
    descriptor = serializers.Field('__str__')

    class Meta:
        model = TaxScheme
        exclude = ['company']

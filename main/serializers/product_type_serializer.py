from rest_framework import serializers
from main.models import ProductType

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

    def create(self, validated_data):
        return ProductType.objects.create(**validated_data)

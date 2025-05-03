from rest_framework import serializers
from main.models import Giftcard

class GiftcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Giftcard
        fields = '__all__'

    def create(self, validated_data):
        return Giftcard.objects.create(**validated_data)

from rest_framework import serializers
from django.contrib.auth import get_user_model
from main.models import Giftcard

User = get_user_model()

class GiftcardSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    total_ammount = serializers.IntegerField()
    message = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Giftcard
        fields = ['email', 'total_ammount', 'message']
    
    def create(self, validated_data):
        recipient_email = validated_data.pop('email')
        to_user = User.objects.get(email=recipient_email)
        
        giftcard = Giftcard.objects.create(
            from_user=self.context['request'].user,
            current_ammount=validated_data['total_ammount'],
            to_user=to_user,
            **validated_data
        )
        return giftcard

class GiftcardRecievedSerializer(serializers.ModelSerializer):
    from_first_name = serializers.CharField(source='from_user.first_name', read_only=True)
    from_last_name = serializers.CharField(source='from_user.last_name', read_only=True)

    class Meta:
        model = Giftcard
        fields = '__all__'


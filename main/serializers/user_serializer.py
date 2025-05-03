from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'phone_number', 'first_name', 'last_name', 'birthday', 'loyalty_points', 'role')  # Add fields you want to expose

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

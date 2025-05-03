from rest_framework import serializers
from django.contrib.auth.models import Group

from main.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birthday', 'password')

    def create(self, validated_data):
        group = Group.objects.filter(name__icontains='Normal').first()
        user = User.objects.create_user(role=group, **validated_data)
        return user


from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['birthday'] = str(user.birthday)
        token['group'] = user.role.name

        # Add any other data you want in the token
        return token


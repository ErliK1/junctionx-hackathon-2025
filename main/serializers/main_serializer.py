from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import Group

from main.models import User

from rest_framework import serializers
from main.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)  # Exclude the password field


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'birthday', 'phone_number', 'password')

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
        token['phone_number'] = user.phone_number
        # Add any other data you want in the token
        return token


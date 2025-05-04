from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import Group

from main.models import User
from main.serializers.main_serializer import UserCreateSerializer, MyTokenObtainPairSerializer, UserProfileSerializer
from main.pagination import CustomPagination

# Create your views here.


@api_view(['GET'])
def test_request(request: Request, *args, **kwargs):
    print(kwargs.get('id'))
    print(request.user)
    return Response({'message': 'hello world'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request: Request):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        response = super(CreateUserView, self).create(request, *args, **kwargs)
        if (response.status_code == status.HTTP_201_CREATED):
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return response


class GetUsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    pagination_class = CustomPagination


@api_view(['post'])
def create_user_groups(request):
    Group.objects.create(name='Normal')
    Group.objects.create(name='Admin')
    Group.objects.create(name='Bartender')
    return Response({'message': 'Done successfully'}, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




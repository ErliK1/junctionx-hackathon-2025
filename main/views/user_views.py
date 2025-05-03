from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from django.contrib.auth import get_user_model
from main.serializers.user_serializer import UserCreateSerializer  # Assuming you have this serializer
from django.shortcuts import get_object_or_404

class UserCreateView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        role_id = request.data.get("role")

        if not role_id or not Group.objects.filter(id=role_id).exists():
            return Response({"message": "Invalid or missing role."}, status=status.HTTP_400_BAD_REQUEST)
        
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return response


class UserDeleteView(DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer  # Use the same serializer to return the user info

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        response = super().destroy(request, *args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(
                {"message": f"User '{user.email}' deleted successfully"},
                status=status.HTTP_200_OK
            )
        return response

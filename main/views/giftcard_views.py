from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from main.models import Giftcard
from main.serializers.giftcard_serializer import GiftcardSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.translation import gettext_lazy as _


class GiftcardCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'total_ammount'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Email of the recipient user'),
                'total_ammount': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total amount of money'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Optional message', default='')
            }
        ),
        responses={201: 'Giftcard created', 400: 'Validation error'}
    )
    
    def post(self, request):
        serializer = GiftcardSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            giftcard = serializer.save()
            return Response({
                'message': 'Giftcard sent successfully!',
                'giftcard_id': giftcard.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GiftcardDeleteView(DestroyAPIView):
    queryset = Giftcard.objects.all()
    serializer_class = GiftcardSerializer

    def destroy(self, request, *args, **kwargs):
        giftcard = self.get_object()
        response = super().destroy(request, *args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(
                {"message": f"Giftcard from '{giftcard.from_user.email}' to '{giftcard.to_user.email}' deleted successfully"},
                status=status.HTTP_200_OK
            )
        return response

from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from main.models import Giftcard, User
from main.serializers.giftcard_serializer import GiftcardSerializer

class GiftcardCreateView(CreateAPIView):
    queryset = Giftcard.objects.all()
    serializer_class = GiftcardSerializer

    def create(self, request, *args, **kwargs):
        from_user_id = request.data.get('from_user')
        to_user_id = request.data.get('to_user')

        if not User.objects.filter(id=from_user_id).exists():
            return Response({"message": "Invalid 'from_user' ID."}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(id=to_user_id).exists():
            return Response({"message": "Invalid 'to_user' ID."}, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response({"message": "Giftcard created successfully"}, status=status.HTTP_201_CREATED)
        return response


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

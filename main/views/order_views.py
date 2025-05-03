from django.db import transaction

from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from main.models import Order, Product
from main.serializers.order_serializer import OrderCreateSerialzer


class CreateSupplyOrder(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = None
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if (not product_id):
            return Response({'message': 'Please provide a product'}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        if not product.product_type.is_deliverable:
            return Response({'message': 'Product is not deliverable', status=status.HTTP_400_BAD_REQUEST})
        order_serializer = OrderCreateSerialzer(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save()
        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)


class CreateNormalOrder(generics.CreateAPIView):
    queryset = Order.objects.all()



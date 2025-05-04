from django.db import transaction

from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from main.models import Order, Product, Option
from main.serializers.order_serializer import OrderCreateSerialzer, OrderCreateSerializerMulti, \
    OrderCreateCustomSerializerMulti, OptionListSerialier, UserOrderListSerializer, OrderUpdateStatusSerializer


class CreateSupplyOrder(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializerMulti
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs):
        order_serializer = OrderCreateSerializerMulti(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save()
        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)


class CreateNormalCustomOrder(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateCustomSerializerMulti

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if (not request.data):
            return Response({'message': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)
        order_serializer = OrderCreateCustomSerializerMulti(data=request.data, context={'request': request})
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save()
        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)


class OptionListApiView(generics.ListAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionListSerialier

class GetUserOrdersView(generics.ListAPIView):
    serializer_class = UserOrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-creation_date')

class GetBartenderOrdersView(generics.ListAPIView):
    serializer_class = UserOrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(is_online=False, status='Pending').order_by('-creation_date')


class OrderUpdateStatusView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateStatusSerializer

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'message': 'Order id is required'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        order.status = 'Finished'
        order.save()
        return Response({'message': 'Order updated successfully'}, status=status.HTTP_200_OK)
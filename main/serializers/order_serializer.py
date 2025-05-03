from rest_framework import serializers
from main.models import Order, Product, Address, OrderItem


class OrderCreateSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'country', 'city', 'street', 'building', 'zip_code')

class OrderCreateSerialzer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    ammount = serializers.DecimalField(max_digits=10, decimal_places=2)
    address = AddressSerializer()


    def create(self, validated_data):
        product: Product = validated_data.get('product')
        address = validated_data.get('address')
        address_obj = Address.objects.create(**address)
        ammount = validated_data.get('amount')
        total_price = product.base_price * ammount
        order = Order.objects.create(total_price=total_price, is_online=True,
                                     address=address)
        order_item = OrderItem.objects.create(product=product, 
                                              total_price=total_price,
                                              total_ammount=ammount,
                                              order=order)
        return order


class OrderCreateSerializerMulti(serializers.Serializer):
    orders = OrderCreateSerialzer(many=True)

    def create(self, validated_data):
        orders = validated_data.get('orders')
        for order in orders:
            product: Product = validated_data.get('product')
            address = validated_data.get('address')
            address_obj = Address.objects.create(**address)
            ammount = validated_data.get('amount')
            total_price = product.base_price * ammount
            order = Order.objects.create(total_price=total_price, is_online=True,
                                         address=address)
            order_item = OrderItem.objects.create(product=product, 
                                                  total_price=total_price,
                                                  total_ammount=ammount,
                                                  order=order)
        return order




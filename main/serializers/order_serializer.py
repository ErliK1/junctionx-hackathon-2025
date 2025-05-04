from rest_framework import serializers
from main.models import Order, Product, Address, OrderItem, Option, OrderOption


class OrderCreateSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'city', 'street', 'building', 'zip_code')


class OrderCreateSerialzer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    ammount = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderCreateSerializerMulti(serializers.Serializer):
    orders = OrderCreateSerialzer(many=True)
    address = AddressSerializer()

    def create(self, validated_data):
        orders = validated_data.get('orders')
        print(orders)
        address = validated_data.get('address')
        address_obj = Address.objects.create(**address)
        order1 = Order.objects.create(total_price=0, is_online=True,
                      address=address_obj)
        all_price = 0
        for order in orders:
            product: Product = order.get('product')
            ammount = order.get('ammount')
            total_price = int(product.base_price * ammount)
            all_price += total_price
            OrderItem.objects.create(product=product,
                                     total_price=total_price,
                                     total_ammount=ammount,
                                     order=order1)
        order1.total_price = all_price
        order1.save()
        return order1


class OrderOptionSerializer(serializers.Serializer):
    option = serializers.PrimaryKeyRelatedField(queryset=Option.objects.all())
    ammount = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderCreateCustomSerializer(serializers.Serializer):
     order_options = OrderOptionSerializer(many=True)
     ammount = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderCreateCustomSerializerMulti(serializers.Serializer):
    normal_orders = OrderCreateSerialzer(many=True, required=False)
    custom_orders = OrderCreateCustomSerializer(many=True, required=False)

    def create(self, validated_data):
        normal_orders_items = validated_data.get('normal_orders')
        custom_orders_items = validated_data.get('custom_orders')
        request = self.context.get('request')
        order = Order.objects.create(total_price=0, is_online=False)
        all_orders_items = self.create_normal_orders(normal_orders_items) + self.create_custom_orders(custom_orders_items)
        total_price = 0
        for order_item in all_orders_items:
            order_item.order = order
            total_price += order_item.total_price
            order_item.save()
        order.total_price = total_price
        if request.user and request.user.is_authenticated:
            order.user = request.user
            request.user.loyalty_points = order.total_price // 7
        order.save()
        return order

    def create_custom_orders(self, custom_orders):
        order_item_list = []
        product = Product.objects.filter(is_customizable=True).first()
        for custom_order in custom_orders:
            order_options = custom_order.get('order_options')
            ammount = custom_order.get('ammount')
            all_price = 0
            order_item = OrderItem.objects.create(product=product, total_price=0, total_ammount=ammount, order_id=0)
            for order_option in order_options:
                option: Option = order_option.get('option')
                option_ammount = order_option.get('ammount')
                total_price = int(option.base_price * (option_ammount / 100))
                all_price += total_price
                OrderOption.objects.create(option=option, order_item=order_item, ammount=option_ammount)
            order_item.total_price = all_price  * ammount
            order_item.save()
            order_item_list.append(order_item)
        return order_item_list

    def create_normal_orders(self, normal_orders):
        order_item_list = []
        for normal_order in normal_orders:
            product: Product = normal_order.get('product')
            ammount = normal_order.get('ammount')
            order_item = OrderItem.objects.create(product=product, total_price=product.base_price * ammount, total_ammount=ammount, order_id=0)
            order_item_list.append(order_item)
        return order_item_list


class OptionListSerialier(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'name', 'type')


class UserOrderListSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'creation_date', 'total_price','order_items']

    def get_order_items(self, obj):
        # Get all order items related to this order
        items = obj.order_items.all()

        result = []
        for item in items:
            item_data = {
                'total_ammount': item.total_ammount,
                'total_price': item.total_price,
                'product': {
                    'name': item.product.name,
                },
            }

            # Get related order options for the item
            order_options = item.order_options.all()
            if order_options:
                item_data['order_options'] = [
                    {
                        'ammount': opt.ammount,
                        'option': {
                            'name': opt.option.name,
                            'base_price': opt.option.base_price,
                        },
                    } for opt in order_options
                ]

            result.append(item_data)

        return result
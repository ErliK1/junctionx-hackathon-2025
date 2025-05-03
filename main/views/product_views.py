from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from main.models import Product, ProductType, Category
from main.serializers.product_serializer import ProductSerializer
from django.shortcuts import get_object_or_404

class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        product_type = request.data.get('product_type')
        category = request.data.get('category')
        
        if not ProductType.objects.filter(id=product_type).exists():
            return Response({"message": "Invalid product type."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Category.objects.filter(id=category).exists():
            return Response({"message": "Invalid category."}, status=status.HTTP_400_BAD_REQUEST)
        
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        return response


class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        response = super().destroy(request, *args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(
                {"message": f"Product '{product.name}' deleted successfully"},
                status=status.HTTP_200_OK
            )
        return response

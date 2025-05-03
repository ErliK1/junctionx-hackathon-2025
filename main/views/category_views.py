from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from main.models import Category
from main.serializers.category_serializer import CategorySerializer
from main.serializers.category_serializer import CategoryWithProductsSerializer
from django.db import models
from main.models import Product
from main.pagination import CustomPagination

class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response({"message": "Category created successfully"}, status=status.HTTP_201_CREATED)
        return response


class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        response = super().destroy(request, *args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(
                {"message": f"Category '{category.name}' deleted successfully"},
                status=status.HTTP_200_OK
            )
        return response


class CategoryListWithProductsView(APIView):
    pagination_class = CustomPagination

    def get(self, request: Request, *args, **kwargs):
        product_type = int(request.query_params.get('is_deliverable'))
        categories = Category.objects.prefetch_related(
            models.Prefetch(
                'products',
                queryset=Product.objects.filter(
                    product_type__is_deliverable=bool(product_type)
                )
            )
        ).all()
        serializer = CategoryWithProductsSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

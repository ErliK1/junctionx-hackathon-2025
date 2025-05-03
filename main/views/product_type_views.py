from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from main.models import ProductType
from main.serializers.product_type_serializer import ProductTypeSerializer

class ProductTypeCreateView(CreateAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response({"message": "Product type created successfully"}, status=status.HTTP_201_CREATED)
        return response


class ProductTypeDeleteView(DestroyAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

    def destroy(self, request, *args, **kwargs):
        product_type = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response(
                {"message": f"Product type '{product_type.name}' deleted successfully"},
                status=status.HTTP_200_OK
            )
        return response

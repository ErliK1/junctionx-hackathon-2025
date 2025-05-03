from django.urls import path
from main.views.category_views import CategoryCreateView, CategoryDeleteView
from main.views.product_views import ProductCreateView, ProductDeleteView
from main.views.user_views import UserCreateView, UserDeleteView
from main.views.product_type_views import ProductTypeCreateView, ProductTypeDeleteView
from main.views.giftcard_views import GiftcardCreateView, GiftcardDeleteView



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('categories/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
    path('products/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    path('product-types/', ProductTypeCreateView.as_view(), name='product-type-create'),
    path('product-types/<int:pk>/', ProductTypeDeleteView.as_view(), name='product-type-delete'),
    path('giftcards/', GiftcardCreateView.as_view(), name='giftcard-create'),
    path('giftcards/<int:pk>/', GiftcardDeleteView.as_view(), name='giftcard-delete'),
]

from django.urls import path
from main.views.category_views import CategoryCreateView, CategoryDeleteView, CategoryListWithProductsView
from main.views.product_views import ProductCreateView, ProductDeleteView
from main.views.product_type_views import ProductTypeCreateView, ProductTypeDeleteView
from main.views.order_views import CreateSupplyOrder, CreateNormalCustomOrder, OptionListApiView, GetUserOrdersView, \
    GetBartenderOrdersView, OrderUpdateStatusView
from main.views.giftcard_views import GiftcardCreateView, GiftcardDeleteView, UserReceivedGiftcardsView



from main.view import test_request, CreateUserView, GetUsersView, create_user_groups, MyTokenObtainPairView, \
    get_current_user, CreateBartenderView, CreateAdminView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('test/<int:id>/', test_request),
    path('create/user/', CreateUserView.as_view()),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get/users/', GetUsersView.as_view()),
    path('user/giftcards', UserReceivedGiftcardsView.as_view(), name='received-giftcards'),
    path('user/profile/', get_current_user),
    path('user/orders/', GetUserOrdersView.as_view(), name='user-orders'),
    path('orders/bartender', GetBartenderOrdersView.as_view(), name='offline-orders'),
    path('create/groups/', create_user_groups),
    path('categories/products/', CategoryListWithProductsView.as_view(), name='category-products'),
    path('categories/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path('product-types/', ProductTypeCreateView.as_view(), name='product-type-create'),
    path('product-types/<int:pk>/', ProductTypeDeleteView.as_view(), name='product-type-delete'),
    path('giftcards/', GiftcardCreateView.as_view(), name='giftcard-create'),
    path('giftcards/<int:pk>/', GiftcardDeleteView.as_view(), name='giftcard-delete'),
    path('create/supply/order/', CreateSupplyOrder.as_view(), name='supply-order-create'),
    path('create/order/', CreateNormalCustomOrder.as_view()),
    path('options/', OptionListApiView.as_view()),
    path('order/complete/', OrderUpdateStatusView.as_view(), name='order-complete'),

    path('create/bartender/', CreateBartenderView.as_view(), name='bartender-create'),

    path('create/admin/', CreateAdminView.as_view(), name='admin-create'),
]

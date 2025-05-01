from django.urls import path

from main.views import test_request, CreateUserView, GetUsersView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('test/<int:id>/', test_request),
    path('create/user/', CreateUserView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get/users/', GetUsersView.as_view())
]

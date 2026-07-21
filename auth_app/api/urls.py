from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, RefreshCookieView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenBlacklistView,

)

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshCookieView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]






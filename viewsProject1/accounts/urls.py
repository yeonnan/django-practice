from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.UserAPIView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('<str:username>/', views.UserDetailAPIView.as_view(), name='profile')
]
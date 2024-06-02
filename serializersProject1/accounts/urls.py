from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.SignupAPIView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # <str:username> 보다 아래에 있으면 password 못먹고 username으로 내려가서 쿼리 매치 못함 오류 뜬다.
    path('password/', views.ChangePasswordAPIView.as_view(), name='change_password'),
    path('<str:username>/', views.UserDetailAPIView.as_view(), name='user_detail'),
]

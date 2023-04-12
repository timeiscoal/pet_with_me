from django.urls import path 
from rest_framework.authtoken.views import obtain_auth_token

from users import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('profile/<user_id>/', views.MyProfileView.as_view()),
    path("me/",views.Me.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('change/<user_id>/', views.ChangePassword.as_view()),
    path('login/', views.LogInView.as_view()),
    path('logout/', views.LogOutView.as_view()),

    path("token_login/", obtain_auth_token),
    path("jwt_login/", views.JWTLogin.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/register/", views.RegisterAPIView.as_view(),),
    path("api/register/login/",views.SimpleJwtLoginView.as_view(),),
    path("api/register/logout/", views.SimpleJWTLogOutView.as_view(),),


]

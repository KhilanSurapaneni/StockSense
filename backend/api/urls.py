from django.urls import path
from .views import CreateUserView, UserProfileActions, ChangePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"), # allows a user to register
    path("token/", TokenObtainPairView.as_view(), name="login"), # allows a user to login
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"), # allows a user to refresh their JWT tokens, so they dont have to continuously login
    path("profile/", UserProfileActions.as_view(), name="profile-actions"), # allows a user to view, update, and delete their OWN profile only
    path("password/change/", ChangePasswordView.as_view(), name="password-change"), # allows a user to change their password
]

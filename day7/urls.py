from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken, obtain_jwt_token

from day7 import views

urlpatterns = [
    url(r"login/", ObtainJSONWebToken.as_view()),
    url(r"obtain/", obtain_jwt_token),
    path("user/", views.UserDetailAPIView.as_view()),
    path("check/", views.LoginAPIView.as_view()),
path("computers/", views.ComputerListAPIView.as_view()),
]
import re

from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from day7.authentication import JWTAuthentication
from day7.filter import ComputerFilterSet, LimitFilter
from day7.models import User, Computer
from day7.serializers import UserModelSerializer, ComputerModelSerializer
from utils.response import APIResponse


class UserDetailAPIView(APIView):
    # 只能登录后才能访问
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        return APIResponse(request={"username": request.user.username})


# 多方式登录
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        account = request.data.get("account")
        pwd = request.data.get("pwd")
        user_ser = UserModelSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)
        return APIResponse(data_message="ok", token=user_ser.token, results=UserModelSerializer(user_ser.obj).data)

    # 面向过程的写法
    def demo_post(self, request, *args, **kwargs):
        account = request.data.get("account")
        pwd = request.data.get("pwd")

        if re.match(r'.+@.+', account):
            user_obj = User.objects.filter(email=account).first()
        elif re.match(r'1[3-9][0-9]{9}', account):
            user_obj = User.objects.filter(phone=account).first()
        else:
            user_obj = User.objects.filter(username=account).first()

        if user_obj and user_obj.check_password(pwd):
            # 签发token
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            print(payload, token)
            return APIResponse(results={"username": user_obj.username}, token=token)

        return APIResponse(data_message="出错了")


# 游标分页
class ComputerListAPIView(ListAPIView):
    queryset = Computer.objects.all()
    serializer_class = ComputerModelSerializer

    # 通过此参数配置过滤的器类
    filter_backends = [SearchFilter, OrderingFilter, LimitFilter, DjangoFilterBackend]
    # 指定当前搜索条件
    search_fields = ["name", "price"]
    # 指定排序的条件
    ordering = ["price"]

    # django-filter 查询   通过filter_class指定过滤器
    filter_class = ComputerFilterSet

    # 指定分页器   不能使用列表 或 元祖指定
    # pagination_class = MyPageNumberPagination
    # pagination_class = MyLimitPagination
    # 127.0.0.1:8000/api/computers/?ordering=price&page_size=1&name=小米
    # pagination_class = MyCoursePagination

import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.settings import api_settings

from day7.models import User, Computer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserModelSerializer(ModelSerializer):
    # write_only只参与反序列化
    account = serializers.CharField(write_only=True)
    pwd = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["account", "pwd", "username", "phone", "email"]

        extra_kwargs = {
            "username": {
                "read_only": True,
            },
            "phone": {
                "read_only": True,
            },
            "email": {
                "read_only": True,
            }

        }

    def validate_account(self, value):
        return value

    def validate_pwd(self, value):
        return value

    def validate(self, attrs):
        account = attrs.get("account")
        pwd = attrs.get("pwd")

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
            self.token = token
            self.obj = user_obj

        return attrs


class ComputerModelSerializer(ModelSerializer):
    class Meta:
        model = Computer
        fields = ("name", "price", "brand")

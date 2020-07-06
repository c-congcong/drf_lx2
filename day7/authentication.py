import jwt
from rest_framework import exceptions
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication, jwt_decode_handler


class JWTAuthentication(BaseJSONWebTokenAuthentication):

    def authenticate(self, request):

        # jwt_value = self.get_jwt_value(request)
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        token = self.parse_jwt_token(jwt_token)

        if token is None:
            return None

        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed("签名过期了")
        except:
            raise exceptions.AuthenticationFailed("非法用户")

        user = self.authenticate_credentials(payload)

        return user, token

    def parse_jwt_token(self, jwt_token):
        tokens = jwt_token.split()
        if len(tokens) != 3 or tokens[0].lower() != "auth" or tokens[2].lower() != "jwt":
            return None

        return tokens[1]

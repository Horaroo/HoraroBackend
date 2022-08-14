from .models import CustomToken
from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    # pass
    model = CustomToken

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is not None:
            user, token = result
            token.save()
            return token, user

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import exceptions
from .models import Token

class TokenAuthentication(BaseAuthentication) : 
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if token : 
            try : 
                user = Token.objects.get(token = str(token).split()[1]).user
            except : 
                raise exceptions.AuthenticationFailed('unauthenticated_user')
        else : 
            user = None

        return user,None
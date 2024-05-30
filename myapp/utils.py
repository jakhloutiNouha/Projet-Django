import uuid
from .models import Token
from django.http import JsonResponse


def new_token() : 
    token = uuid.uuid1().hex
    return token
def token_response(user):
    token = new_token()
    Token.objects.create(token=token, user=user) 
    response_data = {
        'message': 'login successful',
        'token': token,
        'username' : user.email,
        
    }
    print(token)

    return JsonResponse(response_data)

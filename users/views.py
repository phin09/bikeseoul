import os
import jwt
import json
import bcrypt
import pbkdf2

from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

from .models import User

def login(request):
    print(request.body)
    data = json.loads(request.body)
    try:
        input_account  = data['account']
        input_password = data['password'].encode('utf-8')

    except Exception as error_msg:
        return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

    try:
        user = User.objects.get(username=input_account)
    except User.DoesNotExist:
        return JsonResponse({'message': 'INVALID_USER'}, status = 400)

    # if bcrypt.checkpw(input_password, user.password.encode('utf-8')):
    #     SECRET = os.environ.get('DJANGO_SECRET_KEY')
    #     ALGORITHM = os.environ.get('ALGORITHM')
    #     access_token = jwt.encode({'id':user.id}, SECRET, algorithm=ALGORITHM)

    if check_password(input_password, user.password):
        return JsonResponse({'message': 'SUCCESS', 'access_token': access_token.decode('utf-8')}, status = 200)

    return JsonResponse({'message': 'INVALID PASSWORD OR ACCOUNT'}, status = 400)
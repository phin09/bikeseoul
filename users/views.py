import os
import json
import jwt
import bcrypt

from django.shortcuts import render
from django.http import JsonResponse

from .models import User

def login(self, request):
    data = json.loads(request.body)
    try:
        input_account  = data['account']
        input_password = data['password'].encode('utf-8')
    except Exception as error_msg:
        return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

    try:
        user = User.objects.get(email=input_account)
    except User.DoesNotExist:
        return JsonResponse({'message': 'INVALID_USER'}, status = 400)

    if bcrypt.checkpw(input_password, user.password.encode('utf-8')):
        SECRET = os.environ.get('DJANGO_SECRET_KEY')
        ALGORITHM = os.environ.get('ALGORITHM')
        access_token = jwt.encode({'id':user.id}, SECRET, algorithm=ALGORITHM)
        return JsonResponse({'message': 'SUCCESS', 'access_token': access_token.decode('utf-8')}, status = 200)
    return JsonResponse({'message': 'INVALID PASSWORD OR ACCOUNT'}, status = 400)
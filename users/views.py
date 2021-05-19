import os
import jwt
import json

from jwt import algorithms
import bcrypt
import pbkdf2

from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.http import JsonResponse

from .models import User

def login_view(request):
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

    if check_password(input_password, user.password):
        SECRET = os.environ.get('DJANGO_SECRET_KEY')
        ALGORITHM = os.environ.get('ALGORITHM')
        access_token = jwt.encode({'id':user.id}, SECRET, algorithm=ALGORITHM)
        request.session[user.id] = 'login'
        return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status = 200)
    return JsonResponse({'message': 'INVALID PASSWORD OR ACCOUNT'}, status = 400)


def logout_view(request):
    data = json.loads(request.body)
    access_token = data.get('access_token', None)
    if not access_token:
        return JsonResponse({'message': 'Empty Token'}, status = 400)
    
    SECRET = os.environ.get('DJANGO_SECRET_KEY')
    ALGORITHM = os.environ.get('ALGORITHM')

    try:
        payload = jwt.decode(access_token, SECRET, algorithms=[ALGORITHM])
    except jwt.exceptions.InvalidSignatureError:
        return JsonResponse({'message':'Signature Verification Failed'}, status=401)

    user_id = payload['id']
    try:
        del request.session[str(user_id)]
    except KeyError:
        return JsonResponse({'messsage':"User is already logged out"} , status=200)

    return JsonResponse({'message':'User is logged out Successfully'}, status=200)
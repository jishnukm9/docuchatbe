from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes,parser_classes
from .serializers import *
from django.contrib.auth import logout 
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from urllib.request import urlopen
from datetime import datetime,timedelta
from django.db.models import F,Q
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import ast
# Load the environment variables
load_dotenv()


class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'



# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = User.objects.get(username=request.data['username'])
#         user.set_password(request.data['password'])
#         user.save()
#         return Response({'user':serializer.data})
#     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        # token = Token.objects.create(user=user)
        # return Response({'token':token.key,'user':serializer.data})
        return Response({'user':serializer.data})
    else:
        print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login(request):
    user = User.objects.filter(username=request.data['username']).first()
    if not user:
        return Response({"Response":"Not found."},status=status.HTTP_404_NOT_FOUND)
    if not user.check_password(request.data['password']):
        return Response({"Response":"Not found."},status=status.HTTP_404_NOT_FOUND)
    token,_ = Token.objects.get_or_create(user=user)

    serializer = UserSerializer(instance=user)
    data={}
    data['id']=user.id
    data['username']=user.username
    data['email']=user.email
    return Response({"Response":"Logged in successfully",'Token':str(token),"User":data},status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def testing(request):


    return Response({"Response":"token authentication successfull"},status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # Assume the user is already authenticated and a token exists
    try:
        if 'chat_history' in request.session:
            del request.session['chat_history']
            request.session.modified = True
        token = Token.objects.get(user=request.user)
        token.delete()  # Delete the token to effectively "log out" the user

        return Response({"Response": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"Response": "Invalid request or Token not found."}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def chat_stream(request):

    
    message = request.data['message']

    genai.configure(api_key=os.getenv('api_key'))

    model = genai.GenerativeModel('gemini-pro')
    
    if 'chat_history' in request.session:
        chat_history = json.loads(request.session['chat_history'])
        chat = model.start_chat(history=chat_history["history"])
    else:
        chat = model.start_chat()
        chat_history = chat.history

    response = chat.send_message(message)
    response.resolve()


    chat_hostory_list = []
    for item in chat.history:
        dic = {}
        dic['role'] = item.role
        dic['parts'] = [item.parts[0].text]
        chat_hostory_list.append(dic)
     
    
    request.session['chat_history'] = json.dumps({"history":chat_hostory_list})
    request.session.modified = True


    return Response({"Response": chat_hostory_list}, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([BearerTokenAuthentication])
@permission_classes([IsAuthenticated])
def creati_verse(request):

    message = request.data['message']
    
    genai.configure(api_key=os.getenv('api_key'))

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(message)

    return Response({"Response":response.text},status=status.HTTP_200_OK)
